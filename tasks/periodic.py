#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import json
import collections
import traceback

from urllib import request, parse
from urllib.error import HTTPError

from pymongo import DESCENDING

from .celery import celery

from ..models import database
from ..models import User, Weibo


logger = celery.log.get_default_logger()


@celery.task(ignore_result=True)
def user_update():
    try:
        user_records = database[User._name].find()

        for user_record in user_records:
            try:
                if not user_record['access_token']:
                    continue

                _params = { 'access_token': user_record['access_token'] }
                _api = 'https://api.weibo.com/oauth2/get_token_info'
                with request.urlopen(_api, data=parse.urlencode(_params).encode('utf-8')) as f:
                    data = json.loads(f.read().decode('utf-8'))

                if not data.get('expire_in') or data['expire_in'] < 60 * 60:
                    database[User._name].update({'uid': user_record['uid']}, {'$set': {'access_token': None}})
                    continue

                _query = { 'uid': user_record['uid'], 'access_token': user_record['access_token'] }
                _url = 'https://api.weibo.com/2/users/show.json?%s' % parse.urlencode(_query)
                with request.urlopen(_url) as f:
                    data = json.loads(f.read().decode('utf-8'))

                user_model = User(record=user_record, **data)
                database[User._name].update({'uid': user_model.uid}, user_model.to_dict())
            except HTTPError:
                pass
            except:
                traceback.print_exc()
    except Exception as e:
        traceback.print_exc()
        logger.error(e, exc_info=True)


@celery.task(ignore_result=True)
def weibo_update():
    try:
        user_records = database[User._name].find()

        for user in user_records:
            try:
                if not user['access_token']:
                    continue

                weibo_record = database[Weibo._name].find_one(
                    {'uid': user['uid']},
                    sort=[('wid', DESCENDING)],
                )

                _query = {
                    'access_token': user['access_token'],
                    'uid': user['uid'],
                    'since_id': weibo_record['wid'] if weibo_record else 0,
                    'count': 100,
                    'page': 1,
                    'trim_user': 1,
                }
                _url = 'https://api.weibo.com/2/statuses/user_timeline.json?%s' % parse.urlencode(_query)
                with request.urlopen(_url) as f:
                    data = json.loads(f.read().decode('utf-8'))

                weibo_models = [ Weibo(**w) for w in data['statuses'] ]
                weibo_models.reverse()

                if weibo_models:
                    weibo_dicts = [ m.to_dict() for m in weibo_models ]
                    database[Weibo._name].insert(weibo_dicts)
            except HTTPError:
                pass
            except:
                traceback.print_exc()
    except Exception as e:
        traceback.print_exc()
        logger.error(e, exc_info=True)


@celery.task(ignore_result=True)
def weibo_scan():
    try:
        user_records = database[User._name].find(
            {'access_token': {'$exists': True}},
            {'uid': True, 'access_token': True},
        )

        BULK_SIZE = 100
        QUERY_LIMIT = 1000
        for user in user_records:
            logger.info('[W SCAN] %s' % user['uid'])

            weibo_records = database[Weibo._name].find(
                {'uid': user['uid']},
                {'wid': True},
                sort=[('create_date', DESCENDING)],
                limit=QUERY_LIMIT,
            )
            weibo_ids = [ r['wid'] for r in weibo_records ]

            for i in range(math.ceil(len(weibo_ids) / BULK_SIZE)):
                try:
                    _start = i * BULK_SIZE
                    _end = _start + BULK_SIZE
                    _query = {
                        'access_token': user['access_token'],
                        'ids': ','.join(weibo_ids[_start:_end]),
                    }
                    _url = 'https://api.weibo.com/2/statuses/count.json?%s' % parse.urlencode(_query)
                    with request.urlopen(_url) as f:
                        data = json.loads(f.read().decode('utf-8'))

                    for d in data:
                        database[Weibo._name].update(
                            {'wid': str(d['id'])},
                            {'$set': {
                                'comments_count': d['comments'],
                                'reposts_count': d['reposts'],
                                'attitudes_count': d['attitudes'],
                            }},
                        )
                except HTTPError:
                    pass
                except Exception as e:
                    traceback.print_exc()
                    logger.warn(e, exc_info=True)
    except Exception as e:
        traceback.print_exc()
        logger.error(e, exc_info=True)


@celery.task(ignore_result=True)
def weibo_delete():
    try:
        weibo_records = database[Weibo._name].find(
            {'reposts_count': {'$gt': 499}},
            {'wid': True, 'uid': True},
            sort=[('reposts_count', DESCENDING)],
        )

        weibo_grouped = collections.defaultdict(list)
        for weibo in weibo_records:
            weibo_grouped[weibo['uid']].append(weibo['wid'])
        user_records = database[User._name].find({'uid': {'$in': list(weibo_grouped.keys())}})
        user_tokens = dict([ (u['uid'], u['access_token']) for u in user_records if u['options']['delete'] ])

        for uid, access_token in user_tokens.items():
            if not access_token:
                continue

            weibos = weibo_grouped[uid]
            for wid in weibos:
                try:
                    _param = {
                        'access_token': access_token,
                        'id': wid,
                    }
                    _api = 'https://api.weibo.com/2/statuses/destroy.json'
                    with request.urlopen(_api, data=parse.urlencode(_param).encode('utf-8')) as f:
                        data = json.loads(f.read().decode('utf-8'))

                    database[Weibo._name].remove({'wid': data['idstr']})
                except HTTPError:
                    pass
                except:
                    traceback.print_exc()
    except Exception as e:
        traceback.print_exc()
        logger.error(e, exc_info=True)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import json
import datetime
import logging
import traceback

from urllib.parse import urlencode

from pymongo import DESCENDING

from tornado.web import asynchronous
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.stack_context import ExceptionStackContext

from .utils import T, flatten_arguments

from ..conf import setting
from ..models import database, cache
from ..models import Session, User, Weibo, Emotion


logger = logging.getLogger('tornado.general')


class RESTHandler(RequestHandler):
    def restful(self, data):
        self.set_header('Cache-Control', 'private, no-cache')
        self.set_header('Date', datetime.datetime.now())
        self.set_header('Content-Type', 'application/json; charset=utf-8')

        response = {
            'status': 'OK',
            'data': data,
        }

        self.write(json.dumps(response))
        self.finish()


class UserInfoHandler(RESTHandler):
    @asynchronous
    def get(self):
        try:
            session_id = T(self.get_secure_cookie(setting.SESSION_COOKIE))
            session_cache = T(cache.get(session_id.decode('ascii')))
            self.session = Session(**session_cache)
            user_record = T(database[User._name].find_one({'uid': self.session.uid}))

            self.user = User(record=user_record)

            _query = {'uid': self.user.uid, 'access_token': self.user.access_token}
            _url = 'https://api.weibo.com/2/users/show.json?%s' % urlencode(_query)

            request = HTTPRequest(url=_url, method='GET', use_gzip=True)

            with ExceptionStackContext(self._on_exception):
                AsyncHTTPClient().fetch(request, self._on_response)
        except Exception:
            traceback.print_exc()
            self.send_error(400)

    def _on_response(self, response):
        data = json.load(io.TextIOWrapper(response.buffer, encoding='utf-8'))

        user_model = User(record=self.user._record, **data)
        database[User._name].update({'uid': user_model.uid}, user_model.to_dict())

        self.restful(user_model.to_dict(excludes=['_id', 'access_token']))

    def _on_exception(self, *exc_info):
        logger.error('UserInfoHandler: %s' % exc_info[1], exc_info=True)
        self.send_error(500)

        return True


class UserOptionHandler(RESTHandler):
    def post(self):
        try:
            session_id = T(self.get_secure_cookie(setting.SESSION_COOKIE))
            session_cache = T(cache.get(session_id.decode('ascii')))
            self.session = Session(**session_cache)
            user_record = T(database[User._name].find_one({'uid': self.session.uid}))

            options = user_record['options']
            options['delete'] = not options['delete']

            database[User._name].update(
                {'uid': user_record['uid']},
                {'$set': {'options.delete': options['delete']}},
            )

            self.restful(options)
        except Exception:
            traceback.print_exc()
            self.send_error(400)


class WeiboPublicHandler(RESTHandler):
    def get(self):
        try:
            weibo_records = database[Weibo._name].find(
                {},
                sort=[('reposts_count', DESCENDING)],
                limit=6,
            )
            weibo_models = [Weibo(record=r) for r in weibo_records]
            weibo_users = list(set([w.uid for w in weibo_models]))
            user_records = database[User._name].find({'uid': {'$in': weibo_users}})
            user_names = dict([(u['uid'], u['name']) for u in user_records])
            weibo_dicts = [m.to_dict() for m in weibo_models]
            for d in weibo_dicts:
                d['uname'] = user_names.get(d['uid'])

            self.restful(weibo_dicts)
        except Exception:
            traceback.print_exc()
            self.send_error(400)


class WeiboSyncHandler(RESTHandler):
    @asynchronous
    def post(self):
        try:
            session_id = T(self.get_secure_cookie(setting.SESSION_COOKIE))
            session_cache = T(cache.get(session_id.decode('ascii')))
            self.session = Session(**session_cache)
            user_record = T(database[User._name].find_one({'uid': self.session.uid}))

            user = User(record=user_record)

            weibo_record = database[Weibo._name].find_one(
                {'uid': user.uid},
                sort=[('wid', DESCENDING)],
            )

            _query = {
                'access_token': user.access_token,
                'uid': user.uid,
                'since_id': weibo_record['wid'] if weibo_record else 0,
                'count': 100,
                'page': 1,
                'trim_user': 1,
            }
            _url = 'https://api.weibo.com/2/statuses/user_timeline.json?%s' % urlencode(_query)

            request = HTTPRequest(url=_url, method='GET', use_gzip=True)

            with ExceptionStackContext(self._on_exception):
                AsyncHTTPClient().fetch(request, self._on_response)
        except Exception:
            traceback.print_exc()
            self.send_error(400)

    def _on_response(self, response):
        data = json.load(io.TextIOWrapper(response.buffer, encoding='utf-8'))

        weibo_models = [Weibo(**w) for w in data['statuses']]
        weibo_models.reverse()

        if weibo_models:
            weibo_dicts = [m.to_dict() for m in weibo_models]
            database[Weibo._name].insert(weibo_dicts)

        self.restful({'count': len(weibo_models)})

    def _on_exception(self, *exc_info):
        logger.error('UserInfoHandler: %s' % traceback.format_exception(*exc_info)[-1])
        self.send_error(500)

        return True


class WeiboQueryHandler(RESTHandler):
    def get(self):
        try:
            request_args = flatten_arguments(self.request.arguments)

            session_id = T(self.get_secure_cookie(setting.SESSION_COOKIE))
            session_cache = T(cache.get(session_id.decode('ascii')))
            self.session = Session(**session_cache)
            user_record = T(database[User._name].find_one({'uid': self.session.uid}))

            user = User(record=user_record)

            _spec = {'uid': user.uid}
            _limit = request_args.get('limit', 63)

            weibo_records = database[Weibo._name].find(
                _spec,
                sort=[('wid', DESCENDING)],
                limit=_limit,
            )

            weibo_models = [Weibo(record=r) for r in weibo_records]
            weibo_dicts = [m.to_dict() for m in weibo_models]

            self.restful(weibo_dicts)
        except Exception:
            traceback.print_exc()
            self.send_error(400)


class WeiboRedirectHandler(RequestHandler):
    @asynchronous
    def get(self):
        try:
            request_args = flatten_arguments(self.request.arguments)

            session_id = T(self.get_secure_cookie(setting.SESSION_COOKIE))
            session_cache = T(cache.get(session_id.decode('ascii')))
            self.session = Session(**session_cache)
            user_record = T(database[User._name].find_one({'uid': self.session.uid}))

            user = User(record=user_record)

            _query = {
                'access_token': user.access_token,
                'id': request_args['wid'],
                'type': 1,
            }
            _url = 'https://api.weibo.com/2/statuses/querymid.json?%s' % urlencode(_query)

            request = HTTPRequest(url=_url, method='GET', use_gzip=True)

            with ExceptionStackContext(self._on_exception):
                AsyncHTTPClient().fetch(request, self._on_response)
        except Exception:
            traceback.print_exc()
            self.send_error(400)

    def _on_response(self, response):
        data = json.load(io.TextIOWrapper(response.buffer, encoding='utf-8'))

        _url = 'http://weibo.com/%(uid)s/%(mid)s' % {
            'uid': self.session.uid,
            'mid': data['mid'],
        }

        self.redirect(_url)

    def _on_exception(self, *exc_info):
        logger.error('UserInfoHandler: %s' % exc_info[1], exc_info=True)
        self.send_error(500)

        return True


class EmotionQueryHandler(RESTHandler):
    def get(self):
        try:
            def emotion_validator(phrase):
                try:
                    return phrase[0] == '[' and phrase[-1] == ']' and len(phrase) < 10
                except:
                    return False

            emotion_query = self.get_arguments('phrases')
            print(emotion_query)
            emotion_phrases = list(filter(emotion_validator, emotion_query))

            emotion_records = database[Emotion._name].find({'phrase': {'$in': emotion_phrases}})

            emotion_dict = dict([(r['phrase'], r['url']) for r in emotion_records])

            self.restful(emotion_dict)
        except Exception:
            traceback.print_exc()
            self.send_error(400)

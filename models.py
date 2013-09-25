#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
# import traceback

from datetime import datetime

import pymongo
import memcache

from tornado.util import ObjectDict

from .conf import setting
from .utils import generate_key, validate_sha1


class Session(ObjectDict):
    @classmethod
    def create_session(cls):
        return cls(session_id=generate_key(), create_date=datetime.now())

    @classmethod
    def validate(cls, session_id):
        return validate_sha1(session_id)


class MongoBase():
    _name = None
    _attrs = []
    _defaults = {}

    def __init__(self, record=None, **kwargs):
        self.__dict__['_record'] = record or {'_id': None}
        for key, attr in self._attrs:
            if key in kwargs:
                self._record[attr] = kwargs.get(key, self._defaults.get(key))
        self._init_hook()

    def _init_hook(self):
        pass

    def __getattr__(self, name):
        try:
            return self._record[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self._record[name] = value

    def to_dict(self, excludes=['_id', ]):
        record = self._record.copy()
        for key in excludes:
            del record[key]
        return record

    def to_json(self, *args, **kwargs):
        return json.dumps(self.to_dict(*args, **kwargs))


class User(MongoBase):
    _name = 'user'
    _attrs = [
        ('idstr', 'uid'),                             # UID
        ('screen_name', 'user_name'),                 # 昵称
        ('name', 'name'),                             # 友好显示名称 (?)
        ('gender', 'gender'),                         # 性别 m/f/n
        ('province', 'province'),                     # 省级ID
        ('city', 'city'),                             # 城市ID
        ('location', 'location'),                     # 所在地
        ('description', 'description'),               # 个人描述
        ('url', 'website_url'),                       # 博客地址
        ('profile_url', 'profile_url'),               # 微博地址
        ('domain', 'domain'),                         # 个性化域名
        ('weihao', 'weihao'),                         # 微号
        ('profile_image_url', 'avatar_small'),        # 头像地址(小)
        ('avatar_large', 'avatar_large'),             # 头像地址(中)
        ('avatar_hd', 'avatar_hd'),                   # 头像地址(大)
        ('cover_image', 'cover_image'),               # 封面图片
        ('friends_count', 'friends_count'),           # 关注数
        ('followers_count', 'followers_count'),       # 粉丝数
        ('bi_followers_count', 'bi_followers_count'),   # 互粉数
        ('statuses_count', 'statuses_count'),         # 微博数
        ('favourites_count', 'favourites_count'),     # 收藏数
        ('created_at', 'register_date'),              # 微博注册时间
        ('allow_all_act_msg', 'allow_msg'),           # 是否允许所有人私信
        ('allow_all_comment', 'allow_comment'),       # 是否允许所有人评论
        ('geo_enabled', 'geo_enabled'),               # 是否允许标识地理位置
        ('verified', 'verified'),                     # 是否认证用户
    ]

    def _init_hook(self):
        try:
            if isinstance(self.register_date, str):
                self.register_date = datetime.strptime(self.register_date, '%a %b %d %H:%M:%S %z %Y').timestamp()
        except:
            self.register_date = None

        if not hasattr(self, 'options'):
            self.options = {
                'delete': False,
                'warn': False,
            }


class Weibo(MongoBase):
    _name = 'weibo'
    _attrs = [
        ('uid', 'uid'),                         # 用户ID
        ('idstr', 'wid'),                       # 微博ID
        ('mid', 'mid'),                         # 微博MID
        ('text', 'text'),                       # 微博内容
        ('retweeted_status', 'retweeted'),      # 转发原微博
        ('source', 'source'),                   # 微博来源
        ('favorited', 'favorited'),             # 是否已收藏
        ('truncated', 'truncated'),             # 是否被截断
        ('thumbnail_pic', 'thumbnail_pic'),     # 缩略图地址
        ('bmiddle_pic', 'middle_pic'),          # 中等尺寸图片地址
        ('original_pic', 'original_pic'),       # 原始图片地址
        ('pic_urls', 'pic_urls'),               # 配图地址数组
        ('geo', 'geo'),                         # 地理位置信息结构
        ('reposts_count', 'reposts_count'),     # 转发数
        ('comments_count', 'comments_count'),   # 评论数
        ('attitudes_count', 'attitudes_count'),     # 表态数
        ('visible', 'visible'),                 # 可见性
        ('created_at', 'create_date'),          # 微博创建时间
    ]

    def _init_hook(self):
        try:
            if isinstance(self.create_date, str):
                self.create_date = datetime.strptime(self.create_date, '%a %b %d %H:%M:%S %z %Y').timestamp()
        except:
            self.create_date = None

        if isinstance(self.uid, int):
            self.uid = str(self.uid)

        try:
            if isinstance(self.retweeted, dict):
                self.retweeted = self.retweeted['idstr']
        except:
            self.retweeted = None


class Emotion(MongoBase):
    _name = 'emotion'
    _attrs = [
        ('category', 'category'),
        ('common', 'common'),
        ('icon', 'icon'),
        ('phrase', 'phrase'),
        ('picid', 'picid'),
        ('type', 'type'),
        ('url', 'url'),
        ('value', 'value'),
    ]


client = pymongo.MongoClient(setting.MONGO_URL, setting.MONGO_PORT)
database = client[setting.MONGO_DB]

database[User._name].ensure_index([('uid', pymongo.ASCENDING)], unique=True)
database[User._name].ensure_index([('access_token', pymongo.ASCENDING)], unique=True)
database[Weibo._name].ensure_index([('wid', pymongo.ASCENDING)], unique=True)
database[Weibo._name].ensure_index([('uid', pymongo.ASCENDING), ('create_date', pymongo.DESCENDING)])
database[Weibo._name].ensure_index([('retweeted', pymongo.ASCENDING)])
database[Weibo._name].ensure_index([('reposts_count', pymongo.DESCENDING)])
database[Weibo._name].ensure_index([('comments_count', pymongo.DESCENDING)])
database[Emotion._name].ensure_index([('phrase', pymongo.DESCENDING)])

cache = memcache.Client([setting.MEMCACHED])


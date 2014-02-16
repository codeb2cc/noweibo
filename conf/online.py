#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

APP_KEY = os.environ['WEIBO_KEY']
APP_SECRET = os.environ['WEIBO_SECRET']

COOKIE_SECRET = 'cmL8d`+/v5T:DJrkIZVD?UE#JL00Stjt'

AUTHORIZE_REDIRECT = 'http://noweibo.com/auth/authorize'
REVOKE_REDIRECT = 'http://noweibo.com/'

MONGO_URL = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'noweibo'

CELERY_BROKER = 'redis://localhost:6379/1'
CELERY_BACKEND = 'redis://localhost:6379/1'

MEMCACHED = '127.0.0.1:11211'

SESSION_COOKIE = 'session'
SESSION_EXPIRES_SECONDS = 604800
SESSION_EXPIRES_DAYS = 7

SCHEDULE_PERIODIC = 15


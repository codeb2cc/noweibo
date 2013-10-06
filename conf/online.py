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

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USER = os.environ['RABBIT_USER']
RABBITMQ_PASSWORD = os.environ['RABBIT_PASSWD']

MEMCACHED = '127.0.0.1:11211'

SESSION_COOKIE = 'session'
SESSION_EXPIRES_SECONDS = 604800
SESSION_EXPIRES_DAYS = 7

SCHEDULE_PERIODIC = 15


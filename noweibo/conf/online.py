#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


APP_IP = os.environ['OPENSHIFT_DIY_IP']
APP_PORT = int(os.environ['OPENSHIFT_DIY_PORT'])

APP_KEY = os.environ['WEIBO_KEY']
APP_SECRET = os.environ['WEIBO_SECRET']

COOKIE_SECRET = 'cmL8d`+/v5T:DJrkIZVD?UE#JL00Stjt'

STATIC_PATH = os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'noweibo/public/dist')

AUTHORIZE_REDIRECT = 'http://noweibo.com/auth/authorize'
REVOKE_REDIRECT = 'http://noweibo.com/'

MONGO_URL = os.environ['OPENSHIFT_MONGODB_DB_URL']
MONGO_PORT = int(os.environ['OPENSHIFT_MONGODB_DB_PORT'])
MONGO_DB = 'noweibo'

MEMCACHED = '/tmp/memcached.sock'

SESSION_COOKIE = 'session'
SESSION_EXPIRES_SECONDS = 604800
SESSION_EXPIRES_DAYS = 7

SCHEDULE_PERIODIC = 15


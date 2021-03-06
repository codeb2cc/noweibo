#!/usr/bin/env python3
# -*- coding: utf-8 -*-

APP_KEY = '66994707'
APP_SECRET = '323631d3d46128ea30605a7732bb6dfd'

COOKIE_SECRET = '2$onW88^G6I=dB4@EwXN1X!QGc&$$tiY'

AUTHORIZE_REDIRECT = 'http://localhost.com/auth/authorize'
REVOKE_REDIRECT = 'http://localhost.com/'

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


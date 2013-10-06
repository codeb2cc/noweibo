#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


APP_IP = '127.0.0.1'
APP_PORT = 8000

APP_KEY = '66994707'
APP_SECRET = '323631d3d46128ea30605a7732bb6dfd'

COOKIE_SECRET = '2$onW88^G6I=dB4@EwXN1X!QGc&$$tiY'

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public/dist')

AUTHORIZE_REDIRECT = 'http://localhost.com/auth/authorize'
REVOKE_REDIRECT = 'http://localhost.com/'

MONGO_URL = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'noweibo'

MEMCACHED = '127.0.0.1:11211'

SESSION_COOKIE = 'session'
SESSION_EXPIRES_SECONDS = 604800
SESSION_EXPIRES_DAYS = 7

SCHEDULE_PERIODIC = 15


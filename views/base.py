import datetime
import logging
import traceback

from tornado.web import RequestHandler
from tornado.template import Loader

from .utils import T

from .. import conf
from ..models import client, database, cache
from ..models import Session, User


logger = logging.getLogger('tornado.general')
templates = Loader('noweibo/templates')


class BaseViewHandler(RequestHandler):
    def on_finish(self):
        self.set_header('Date', datetime.datetime.now())
        self.set_header('Content-Type', 'text/html; charset=utf-8')


class IndexHandler(BaseViewHandler):
    def get(self):
        try:
            session_id   = T(self.get_secure_cookie(conf.SESSION_COOKIE))
            session_cache = T(cache.get(session_id.decode('ascii')))
            self.session = Session(**session_cache)

            self.redirect('/auth/redirect')
            return
        except:
            pass

        tpl = templates.load('index.tpl')
        context = {
            'head_title': 'Noweibo | 莫微博',
            'head_description': 'noweibo.com',
            'angular_module': 'noweiboIndex',
        }
        self.write(tpl.generate(**context))


class HomeHandler(BaseViewHandler):
    def get(self):
        try:
            session_id   = T(self.get_secure_cookie(conf.SESSION_COOKIE))
            session_cache = T(cache.get(session_id.decode('ascii')))
            self.session = Session(**session_cache)
            user_record  = T(database[User._name].find_one({'uid': self.session.uid}))

            assert user_record['access_token']

            tpl = templates.load('home.tpl')
            context = {
                'head_title': 'Noweibo | 莫微博',
                'head_description': 'noweibo.com',
                'angular_module': 'noweiboHome',
            }
            self.write(tpl.generate(**context))
        except (ValueError, AssertionError):
            self.redirect('/auth/redirect')
        except Exception:
            traceback.print_exc()
            self.redirect('/')



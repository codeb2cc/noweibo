import io
import json
import datetime
import logging
import traceback

from urllib.parse import urlencode

from tornado.web import asynchronous
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPResponse, HTTPError
from tornado.gen import coroutine
from tornado.stack_context import ExceptionStackContext

from .utils import T, flatten_arguments

from .. import conf
from .. import tasks
from ..models import client, database, cache
from ..models import Session, User


logger = logging.getLogger('tornado.general')


class OAuth2RedirectHandler(RequestHandler):
    def get(self):
        _client_id = conf.APP_KEY
        _redirect_uri = conf.AUTHORIZE_REDIRECT
        # _scope = None
        # _state = None

        _api = 'https://api.weibo.com/oauth2/authorize'
        _params = {
            'client_id': _client_id,
            'redirect_uri': _redirect_uri,
            }

        self.redirect(_api + '?' + urlencode(_params))


class OAuth2RevokeHandler(RequestHandler):
    @asynchronous
    def get(self):
        try:
            session_id   = T(self.get_secure_cookie(conf.SESSION_COOKIE))
            self.session = T(Session(cache.get(session_id.decode('ascii'))))
            user_record  = T(database[User._name].find_one({'uid': self.session.uid}))

            _query = { 'access_token': user_record['access_token'] }
            _url = 'https://api.weibo.com/oauth2/revokeoauth2?%s' % urlencode(_query)

            request = HTTPRequest(url=_url, method='GET', use_gzip=True)

            with ExceptionStackContext(self._on_exception):
                AsyncHTTPClient().fetch(request, self._on_response)
        except Exception:
            traceback.print_exc()
            self.redirect('/')

    def _on_response(self, response):
        database[User._name].update(
            {'uid': self.session.uid},
            {'$set': {'access_token': None}},
        )
        cache.delete(self.session.session_id)

        self.redirect('/')

    def _on_exception(self, *exc_info):
        logger.error('OAuth2RevokeHandler: %s' % exc_info[1], exc_info=True)
        self.send_error(500)


class OAuth2AuthorizeHandler(RequestHandler):
    @coroutine
    def get(self):
        request_args = flatten_arguments(self.request.arguments)

        try:
            _code = request_args['code']
            response = yield self._fetch_access_token(_code)
            data = self._parse_response(response)

            _uid = data['uid']
            _access_token = data['access_token']
            response = yield self._fetch_user_info(_uid, _access_token)
            data = self._parse_response(response)

            user_model = User(**data)
            user_model.access_token = _access_token

            database[User._name].update({'uid': user_model.uid}, user_model.to_dict(), upsert=True)

            session = Session.create_session()
            session.uid = user_model.uid
            session.access_token = user_model.access_token

            cache.set(session.session_id, session, conf.SESSION_EXPIRES_SECONDS)
            self.set_secure_cookie(
                    conf.SESSION_COOKIE,
                    session.session_id,
                    expires_days=conf.SESSION_EXPIRES_DAYS)
            self.redirect('/home')
        except KeyError:
            self.redirect('/')
            return
        except Exception as e:
            logger.warn('OAuth2AuthorizeHandler: %s [code: %s]' % (e, _code))
            self.redirect('/')

    def _fetch_access_token(self, code):
        _api = 'https://api.weibo.com/oauth2/access_token'
        _params = {
            'client_id': conf.APP_KEY,
            'client_secret': conf.APP_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': conf.AUTHORIZE_REDIRECT,
        }
        _request = HTTPRequest(url=_api, method='POST', body=urlencode(_params), use_gzip=True)

        return AsyncHTTPClient().fetch(_request)

    def _fetch_user_info(self, uid, access_token):
        _query = { 'uid': uid, 'access_token': access_token }
        _url = 'https://api.weibo.com/2/users/show.json?%s' % urlencode(_query)
        _request = HTTPRequest(url=_url, method='GET', use_gzip=True)

        return AsyncHTTPClient().fetch(_request)

    def _parse_response(self, response):
        try:
            assert not response.error
            data = json.load(io.TextIOWrapper(response.buffer, encoding='utf-8'))
            assert not data.get('error_code')

            return data
        except (ValueError, AssertionError):
            return None


class OAuth2InfoHandler(RequestHandler):
    @asynchronous
    def get(self):
        request_args = flatten_arguments(self.request.arguments)

        _access_token = request_args['access_token']
        _api = 'https://api.weibo.com/oauth2/get_token_info'
        _params = {
            'access_token': _access_token,
        }

        request = HTTPRequest(url=_api, method='POST', body=urlencode(_params), use_gzip=True)

        with ExceptionStackContext(self._on_exception):
            AsyncHTTPClient().fetch(request, self._on_response)

    def _on_response(self, response):
        self.set_header('Cache-Control', 'private')
        self.set_header('Date', datetime.datetime.now())
        self.set_header('Content-Type', 'application/json; charset=utf-8')

        self.write(response.body)
        self.finish()

    def _on_exception(self, *exc_info):
        logger.error('OAuth2InfoHandler: %s' % exc_info[1], exc_info=True)
        self.send_error(500)
        return




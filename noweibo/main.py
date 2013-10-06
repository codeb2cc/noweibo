#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import traceback

from tornado import options, ioloop, web, process

from . import views
from .conf import setting


options.define('port', default=setting.APP_PORT, type=int)
options.define('process', default=1, type=int)
options.define('debug', default=3, type=int)


def main():
    options.parse_command_line()

    _port = options.options.port
    _process_num = options.options.process
    _debug_level = options.options.debug * 10

    process.fork_processes(_process_num, max_restarts=3)

    process_port = _port + process.task_id()
    process_debug = _process_num <= 1 and _debug_level < 30

    print('Service Running on %d ...' % process_port)

    app = web.Application((
        (r'/', views.base.IndexHandler),
        (r'/home', views.base.HomeHandler),
        (r'/auth/redirect', views.auth.OAuth2RedirectHandler),
        (r'/auth/revoke', views.auth.OAuth2RevokeHandler),
        (r'/auth/authorize', views.auth.OAuth2AuthorizeHandler),
        (r'/auth/info', views.auth.OAuth2InfoHandler),
        (r'/user/info', views.rest.UserInfoHandler),
        (r'/user/option', views.rest.UserOptionHandler),
        (r'/weibo/public', views.rest.WeiboPublicHandler),
        (r'/weibo/sync', views.rest.WeiboSyncHandler),
        (r'/weibo/query', views.rest.WeiboQueryHandler),
        (r'/weibo/redirect', views.rest.WeiboRedirectHandler),
        (r'/emotion/query', views.rest.EmotionQueryHandler),
        (r'/public/(.*)', web.StaticFileHandler, {'path': setting.STATIC_PATH}),
    ), debug=process_debug, cookie_secret=setting.COOKIE_SECRET)
    app.listen(process_port, address=setting.APP_IP, xheaders=True)

    loop = ioloop.IOLoop.instance()
    loop.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if not process.task_id() is None:
            ioloop.IOLoop.current().stop()
        else:
            print('Capture KeyboardInterrupt. Try to stop service ...')


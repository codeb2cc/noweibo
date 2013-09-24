from datetime import timedelta

from celery import Celery

from ..conf import setting

celery = Celery(
    'noweibo',
    broker='amqp://%(user)s:%(password)s@%(host)s:%(port)s//' % {
        'host': setting.RABBITMQ_HOST,
        'port': setting.RABBITMQ_PORT,
        'user': setting.RABBITMQ_USER,
        'password': setting.RABBITMQ_PASSWORD,
    }
)

celery.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_IMPORTS=('noweibo.tasks.periodic', ),
    CELERY_IGNORE_RESULT=True,
    CELERYD_MAX_TASKS_PER_CHILD=100,
    CELERYBEAT_SCHEDULE={
        'user_update': {
            'task': 'noweibo.tasks.periodic.user_update',
            'schedule': timedelta(minutes=setting.SCHEDULE_PERIODIC),
            'args': (),
        },
        'weibo_update': {
            'task': 'noweibo.tasks.periodic.weibo_update',
            'schedule': timedelta(minutes=setting.SCHEDULE_PERIODIC),
            'args': (),
        },
        'weibo_scan': {
            'task': 'noweibo.tasks.periodic.weibo_scan',
            'schedule': timedelta(minutes=setting.SCHEDULE_PERIODIC),
            'args': (),
        },
        'weibo_delete': {
            'task': 'noweibo.tasks.periodic.weibo_delete',
            'schedule': timedelta(minutes=setting.SCHEDULE_PERIODIC),
            'args': (),
        },
    },
    ADMINS=(('Codeb Fan', 'codeb2cc@163.com'), ),
    CELERY_SEND_TASK_ERROR_EMAILS=True,
    SERVER_EMAIL='logentries@163.com',
    EMAIL_HOST='smtp.163.com',
    EMAIL_PORT=25,
    EMAIL_HOST_USER='logentries@163.com',
    EMAIL_HOST_PASSWORD='h7o8o9w1a',
)


if __name__ == '__main__':
    celery.start()


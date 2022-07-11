import os

from pytz import timezone
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.conf.enable_utc = False
app.conf.update(timezone=('Asia/Karachi'))
app.config_from_object('django.conf:settings', namespace='CELERY')

#celery beat settings
#Note: while run celery beat, celery worker will also have to be run on the same machine 
app.conf.beat_schedule = {
    'send-mail-every-day-at-8': {
        'task': 'core.tasks.send_mail_func',
        'schedule': crontab(hour=19, minute=43),
    }
}
#END celery beat settings

app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
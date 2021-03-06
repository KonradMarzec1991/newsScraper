"""
This module contains celery config
"""

from __future__ import (
    absolute_import,
    unicode_literals
)
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'download_news': {
        'task': 'news.tasks.get_news',
        'schedule': crontab(minute='0', hour=settings.INTERVALS)
    },
}
app.conf.timezone = 'Europe/Warsaw'


@app.task(bind=True)
def debug_task(self):
    """Debug function"""
    print(f'Request: {self.request!r}')

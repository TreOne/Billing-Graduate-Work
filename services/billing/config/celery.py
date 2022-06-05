import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config", broker=settings.CELERY_BROKER_URL)

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'add-every-day-autopay': {
        'task': 'tasks.autopay_periodic_task',
        'schedule': crontab(minute=0, hour=0),
        'args': (),
    },
}
app.conf.timezone = settings.TIME_ZONE

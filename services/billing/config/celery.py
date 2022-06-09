import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config", broker=settings.CELERY_BROKER_URL)

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#crontab-schedules
app.conf.beat_schedule = {
    "add-every-day-autopay": {
        "task": "billing.tasks.autopay_periodic_task",
        "schedule": crontab(minute=0, hour=0),
        "args": (),
    },
    "demo": {
        "task": "billing.tasks.say_hello",
        "schedule": crontab(minute="*/1"),
        # "schedule": crontab(minute=0, hour=0),
        "args": (),
    },
}
app.conf.timezone = settings.TIME_ZONE

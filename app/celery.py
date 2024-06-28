import os
from celery import Celery
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")


app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.task_routes = settings.TASK_ROUTER
app.conf.broker_transport_options = settings.BROKER_TRANSPORT_OPTIONS
app.autodiscover_tasks()
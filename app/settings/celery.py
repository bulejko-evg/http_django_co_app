REDIS_HOST = "127.0.0.1"
REDIS_PORT = "6379"
CELERY_BROKER_URL = "redis://"+REDIS_HOST+":"+REDIS_PORT+"/0"
# CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_BACKEND = "redis://"+REDIS_HOST+":"+REDIS_PORT+"/0"

TASK_ROUTER = {
    "app.apps.account.tasks.celery_send_mail": {"queue": "celery:3"},
}
BROKER_TRANSPORT_OPTIONS = {
    "priority_steps": list(range(10)),
    "sep": ":",
    "queue_order_strategy": "priority",
}
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
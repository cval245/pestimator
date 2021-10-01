from celery import Celery
from django.utils.module_loading import import_string
from djmoney import settings
from django.conf import settings

app = Celery('tasks', broker=settings.CELERY_BROKER_URL)


@app.task
def update_rates(backend=settings.EXCHANGE_BACKEND, **kwargs):
    backend = import_string(backend)()
    backend.update_rates(**kwargs)

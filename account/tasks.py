from celery import Celery, shared_task
from django.utils.module_loading import import_string
from djmoney import settings
from django.conf import settings

# app = Celery('tasks', broker=settings.CELERY_BROKER_URL)
app = Celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(40.0, update_rates())


@app.task
def update_rates(**kwargs):
    backend = settings.EXCHANGE_BACKEND
    backend = import_string(backend)()
    backend.update_rates(**kwargs)

from celery import Celery
from django.utils.module_loading import import_string
from djmoney import settings

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def update_rates(backend=settings.EXCHANGE_BACKEND, **kwargs):
    backend = import_string(backend)()
    backend.update_rates(**kwargs)

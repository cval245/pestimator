import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pestimator.settings')

app = Celery('pestimator', broker="amqps://yivfkhqd:WrcWUxS7CP45fshvaNkIhEzEGLJyP6_2@fish.rmq.cloudamqp.com/yivfkhqd")

#app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
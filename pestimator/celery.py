# import os

# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pestimator.settings')

# app = Celery('pestimator')

# app.config_from_object('django.conf:settings', namespace='CELERY')

# app.autodiscover_tasks()
# app.conf.update(BROKER_URL=os.environ['amqps://yivfkhqd:WrcWUxS7CP45fshvaNkIhEzEGLJyP6_2@fish.rmq.cloudamqp.com/yivfkhqd'])

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')



import pika, os, signal, sys

def signal_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqps://yivfkhqd:WrcWUxS7CP45fshvaNkIhEzEGLJyP6_2@fish.rmq.cloudamqp.com/yivfkhqd')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='hello') # Declare a queue
channel.basic_publish(exchange='',
                  routing_key='hello',
                  body='Hello CloudAMQP!')

print(" [x] Sent 'Hello World!'")

def callback(ch, method, properties, body):
  print(" [x] Received " + str(body))

channel.basic_consume('hello',
                      callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()
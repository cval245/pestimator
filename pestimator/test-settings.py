from .settings import * 
DEBUG = True;

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pestimator',
        'USER': 'djangoconnect',
        'HOST': 'localhost',
        'PASSWORD': 'Belgrade2010',
        'PORT': '5432',
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=3),
}

DOMAIN = 'localhost:4200'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.privateemail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'cval.me@patport.cc'
EMAIL_HOST_PASSWORD = 'xZmLvUYiKlR51j7yu9N2'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = 'cval.me@patport.cc'


# BROKER_URL = os.environ.get("amqps://yivfkhqd:WrcWUxS7CP45fshvaNkIhEzEGLJyP6_2@fish.rmq.cloudamqp.com/yivfkhqd", "django://")
# BROKER_POOL_LIMIT = 1
# BROKER_CONNECTION_MAX_RETRIES = 100
# CELERY_BROKER_URL = "amqps://yivfkhqd:WrcWUxS7CP45fshvaNkIhEzEGLJyP6_2@fish.rmq.cloudamqp.com/yivfkhqd"
# CELERY_TASK_SERIALIZER = "json"
# CELERY_ACCEPT_CONTENT = ["json", "msgpack"]
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


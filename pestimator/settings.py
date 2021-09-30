"""
Django settings for pestimator project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import environ
from datetime import timedelta
from pathlib import Path
from . import base_settings

env = environ.Env(DEBUG=(bool, False))
# env = environ.ENV(
#     DEBUG=(bool, False)
# )

BASE_DIR = Path(__file__).resolve().parent.parent
# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from celery.schedules import crontab

ALLOWED_HOSTS = ["pestimator.herokuapp.com"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'HOST': env('DATABASE_HOST'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'PORT': env('DATABASE_PORT')
    }
}

CORS_ALLOWED_ORIGINS = [
    "https://patport.cc",
    "https://www.patport.cc"
]


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

DOMAIN = 'patport.cc'
DOMAIN_FULL = 'https://patport.cc'
SITE_NAME = 'PatPort'

OPEN_EXCHANGE_RATES_APP_ID = env('OPEN_EXCHANGE_RATES_APP_ID')

BROKER_URL = os.environ.get(env('BROKER_PARTIAL_URL'), "django://")
BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_MAX_RETRIES = 100
CELERY_BROKER_URL = env('BROKER_PARTIAL_URL')
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json", "msgpack"]
CELERYBEAT_SCHEDULER = {
    'update_rates': {
        'task': './tasks.py/update_rates',
        'schedule': crontab(minute=0, hour=12),
        'kwargs': {}  # For custom arguments
    }}

STRIPE_PRIVATE_KEY = env('STRIPE_PRIVATE_KEY')


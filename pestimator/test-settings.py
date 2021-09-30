import os
from pathlib import Path

from .base_settings import *

import environ

DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(os.path.join(BASE_DIR, '.env-test'))
SECRET_KEY = env('SECRET_KEY')

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

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
ALLOWED_HOSTS = ["localhost"]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "https://localhost:4200",
]
#
# ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
#
# SIMPLE_JWT = {
#     'AUTH_HEADER_TYPES': ('Bearer'),
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
#     'REFRESH_TOKEN_LIFETIME': timedelta(minutes=600),
# }
#
DOMAIN = 'localhost:4200'
DOMAIN_FULL = 'http://localhost:4200'

OPEN_EXCHANGE_RATES_APP_ID = env('OPEN_EXCHANGE_RATES_APP_ID')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

STRIPE_PRIVATE_KEY = env('STRIPE_PRIVATE_KEY')
#

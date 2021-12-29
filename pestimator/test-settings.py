import os
from pathlib import Path

from .base_settings import *

import environ

DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(os.path.join(BASE_DIR, '.env-test'), overwrite=True)
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
CORS_EXPOSE_HEADERS = ['content-disposition']

DOMAIN = 'localhost:4200'
DOMAIN_FULL = 'http://localhost:4200'

OPEN_EXCHANGE_RATES_APP_ID = env('OPEN_EXCHANGE_RATES_APP_ID')
ANYMAIL = {
    "MAILGUN_API_KEY": env("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": env("MAILGUN_SENDER_DOMAIN"),
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = env('SERVER_EMAIL')

STRIPE_PRIVATE_KEY = env('STRIPE_PRIVATE_KEY')
GOOGLE_RECAPTCHA_SECRET_KEY = env('GOOGLE_RECAPTCHA_SECRET_KEY')
USE_RECAPTCHA_BOOL = True

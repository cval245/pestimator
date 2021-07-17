"""
Django settings for pestimator project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fvr3+$jwp+bv-!nbx(*ld5mv)i5&xbf9=yj9d-61^*7j@&#d@)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["localhost", "pestimator.herokuapp.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'silk',
    'rest_framework',
    'djoser',
    'corsheaders',
    'djmoney',
    'djmoney.contrib.exchange',
    'djcelery_email',
    'account.apps.AccountConfig',
    'application.apps.ApplicationConfig',
    'estimation.apps.EstimationConfig',
    'characteristics.apps.CharacteristicsConfig',
    'family.apps.FamilyConfig',
    'famform.apps.FamformConfig',
    'transform.apps.TransformConfig',
    'lawfirm.apps.LawfirmConfig',
    'user.apps.UserConfig',
    'countryform.apps.CountryformConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    #'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'pestimator.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pestimator.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'pestimator',
#         'USER': 'djangoconnect',
#         'HOST': 'localhost',
#         'PASSWORD': 'Belgrade2010',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'de9ftmo4vm9jj1',
        'USER': 'mzabyikihumhgg',
        'HOST': 'ec2-23-20-124-77.compute-1.amazonaws.com',
        'PASSWORD': '4419a81170245ee8749644f3e5f230f236013784424104661b9e79594569be68',
        'PORT': '5432',
    }
}


AUTH_USER_MODEL = 'user.User'
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
]

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer'),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=600),
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "https://localhost:4200",
    # "https://cval.me",
    # "https://www.cval.me",
    # "https://cval.me",
    # "https://www.cval.me",
    "https://patport.cc",
    "https://www.patport.cc"
]
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
EMAIL_HOST = 'mail.privateemail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'cval.me@patport.cc'
EMAIL_HOST_PASSWORD = 'xZmLvUYiKlR51j7yu9N2'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = 'cval.me@patport.cc'

#DOMAIN = 'localhost:4200'

DOMAIN = 'patport.cc'
SITE_NAME = 'PatPort'
DJOSER = {
    'SEND_ACTIVATION_EMAIL': True,
    'USER_CREATE_PASSWORD_RETYPE': True,
    'ACTIVATION_URL': 'account/activate/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_URL': 'account/password-reset/{uid}/{token}',
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'TOKEN_MODEL': None,
}
OPEN_EXCHANGE_RATES_APP_ID = 'f8873179704e447fb5e75f4543dd98b5'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


BROKER_URL = os.environ.get("amqps://yivfkhqd:WrcWUxS7CP45fshvaNkIhEzEGLJyP6_2@fish.rmq.cloudamqp.com/yivfkhqd", "django://")
BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_MAX_RETRIES = 100
CELERY_BROKER_URL = "amqps://yivfkhqd:WrcWUxS7CP45fshvaNkIhEzEGLJyP6_2@fish.rmq.cloudamqp.com/yivfkhqd"
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json", "msgpack"]
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


#APPEND_SLASH = False;

# LOGGING = {
#     'version': 1,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': './debug.log',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#         },
#     },
# }

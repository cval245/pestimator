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
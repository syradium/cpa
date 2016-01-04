from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_SERVICE'],
        'PORT': os.environ['DB_PORT']
    }
}


CACHES['default']['LOCATION'], CACHES['session']['LOCATION'] =  'redis://localhost:6379/0', 'redis://localhost:6379/1'

ALLOWED_HOSTS = ['*']
STATIC_ROOT = os.environ['STATIC_ROOT']

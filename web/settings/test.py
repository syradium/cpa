from .local import *


CACHES['default']['LOCATION'] = 'redis://redis:6379/9',

BROKER_URL = 'redis://redis:6379/9'
CELERY_RESULT_BACKEND = 'redis://redis:6379/9'
CONSTANCE_REDIS_CONNECTION = 'redis://redis:6379/9'
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

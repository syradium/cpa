from .local import *


CACHES = {
    'default': {
        'BACKEND': 'redis_lock.django_cache.RedisCache',
        'LOCATION': 'redis://redis:6379/9',
        'OPTIONS': {
            'CONNECTION_POOL_KWARGS': {'decode_responses': True},
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': None,
    }
}

BROKER_URL = 'redis://redis:6379/9'
CELERY_RESULT_BACKEND = 'redis://redis:6379/9'
CONSTANCE_REDIS_CONNECTION = 'redis://redis:6379/9'
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

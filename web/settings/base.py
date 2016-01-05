import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SECRET_KEY = os.environ.get('SECRET_KEY', 'some-key')
ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'crispy_forms',
    'djangobower',
    'rest_framework',
    'django_extensions',
    'api',
    'orders',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'api.middleware.MethodOverrideMiddleware',
)

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/0',
        'OPTIONS': {
            'CONNECTION_POOL_KWARGS': {'decode_responses': True},
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': None,
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

WSGI_APPLICATION = 'web.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'session'


STATIC_URL = '/static/'
STATIC_ROOT = '/usr/src/static'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder', 'djangobower.finders.BowerFinder')

BOWER_INSTALLED_APPS = (
    'bootstrap#3.3.6',
    'git://github.com/wenzhixin/bootstrap-table.git#618805c3bb63611a4a52ee4ba4fe28c8474996c6',
    'intercooler-js#0.9.2',
    'jquery#2.1.4',
    'jquery-ui#1.11.4',
    'moment#2.11.0',
    'select2#4.0.1',
    'startbootstrap-sb-admin-2#1.0.8',
    'x-editable#1.5.1',
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
}

METHOD_OVERRIDE_HEADER = 'HTTP_X_HTTP_METHOD_OVERRIDE'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'api': {
            'format': '%(asctime)s %(message)s',
        },
    },
    'handlers': {
        'api_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/api.log',
            'formatter': 'api',
        },
    },
    'loggers': {
        'api': {
            'handlers': ['api_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

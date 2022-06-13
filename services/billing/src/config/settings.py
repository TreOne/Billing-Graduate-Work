import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY: str = os.environ.get('SECRET_KEY')
DEBUG: int = int(os.environ.get('DEBUG', default=0))
IS_LOCAL: int = int(os.environ.get('IS_LOCAL', default=0))

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(' ')

# CELERY CONFIGURATION
# ------------------------------------------------------------------------------
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://billing_redis:6379/0')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TRACK_STARTED = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Django Rest Framework
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    # CORS header
    'corsheaders',
    # Celery
    'django_celery_results',
    'django_celery_beat',
    # Swagger
    'drf_spectacular',
    # Project apps
    'billing',
    # API
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates',],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE'),
        'NAME': os.environ.get('SQL_DATABASE'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
        'HOST': os.environ.get('SQL_HOST'),
        'PORT': os.environ.get('SQL_PORT'),
    },
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# DRF API
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PARSER_CLASSES': ('rest_framework.parsers.JSONParser',),
    # "DEFAULT_RENDERER_CLASSES": (
    #     "rest_framework.renderers.JSONRenderer",
    #     "rest_framework.renderers.BrowsableAPIRenderer",
    # ),
    # "DEFAULT_PERMISSION_CLASSES": (
    #     "rest_framework.permissions.IsAuthenticated",
    #     "rest_framework.permissions.DjangoModelPermissions",
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {'anon': '5/second', 'user': '12/second',},
}

SIMPLE_JWT = {
    'SIGNING_KEY': os.environ.get('JWT_SECRET_KEY'),
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'JTI_CLAIM': 'jti',
    'USER_ID_CLAIM': 'user_uuid',
    'TOKEN_TYPE_CLAIM': 'type',
}

# Swagger
SPECTACULAR_SETTINGS = {
    'TITLE': 'Billing service API',
    'DESCRIPTION': 'Arbeit macht frei',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:5020',
    'http://127.0.0.1:8000',
    'http://localhost:3000',
    'http://localhost:5000',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'timezone',
    'platform',
]

# Internationalization
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_URL: str = os.environ.get('SITE_URL')

# Yookassa
YOOKASSA_SHOP_ID: int = int(os.environ.get('YOOKASSA_SHOP_ID'))
YOOKASSA_SECRET_KEY: str = os.environ.get('YOOKASSA_SECRET_KEY')
YOOKASSA_PAYMENT_RETURN_URL: str = os.environ.get('YOOKASSA_PAYMENT_RETURN_URL')

# KAFKA
KAFKA_HOST = os.environ.get('KAFKA_HOST')
KAFKA_PORT: int = int(os.environ.get('KAFKA_PORT'))

# MOVIE_SERVICE
MOVIE_SERVICE_URL: str = os.environ.get('MOVIE_SERVICE_URL')
MOVIE_SERVICE_GET_MOVIE: str = os.environ.get('MOVIE_SERVICE_GET_MOVIE')

# AUTH_SERVICE
AUTH_SERVICE_USERNAME: str = os.environ.get('AUTH_SERVICE_USERNAME')
AUTH_SERVICE_PASSWORD: str = os.environ.get('AUTH_SERVICE_PASSWORD')
AUTH_SERVICE_URL: str = os.environ.get('AUTH_SERVICE_URL')
AUTH_SERVICE_URL_SUBSCRIPTIONS_END: str = os.environ.get('AUTH_SERVICE_URL_SUBSCRIPTIONS_END')
AUTH_SERVICE_URL_REFRESH: str = os.environ.get('AUTH_SERVICE_URL_REFRESH')
AUTH_SERVICE_URL_LOGIN: str = os.environ.get('AUTH_SERVICE_URL_LOGIN')

# Django Logs
LOGS_BASE_DIR = BASE_DIR / 'logs'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # 'filters': {
    #     'require_debug_false': {
    #         '()': 'django.utils.log.RequireDebugFalse'
    #     }
    # },
    'formatters': {
        'json': {'()': 'ecs_logging.StdlibFormatter'},
        'console': {
            'format': '[%(asctime)s] %(levelname)s|%(name)s|%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'billing_handler': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logging.FileHandler',
            'filename': LOGS_BASE_DIR / 'billing.json',
        },
        'celery_handler': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logging.FileHandler',
            'filename': LOGS_BASE_DIR / 'celery.json',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {'handlers': ['console'], 'level': 'DEBUG',},
        'billing': {'handlers': ['billing_handler'], 'level': 'INFO', 'propagate': True,},
        'celery': {'handlers': ['celery_handler'], 'level': 'INFO', 'propagate': True,},
    },
}

"""
Django settings for conf project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from decouple import config
from django.utils.translation import gettext_lazy as _


""" Base Setting's """
BASE_DIR = Path(__file__).resolve().parent.parent
WSGI_APPLICATION = 'conf.wsgi.application'
ROOT_URLCONF = 'conf.urls'

SECRET_KEY = config('SECRET_KEY', cast=str)

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = \
    ['*'] if DEBUG else config(
            'ALLOWED_HOSTS',
            cast=lambda hosts: [h.strip() for h in hosts.split(",") if h]
        )
# https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


""" App's """
EXTERNAL_APPS_prefix = [
    
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MY_APPS = [
    'apps.core.apps.CoreConfig',
    'apps.posts.apps.PostsConfig',
    'apps.users.apps.UsersConfig',
]

EXTERNAL_APPS_suffix = [

]

INSTALLED_APPS = EXTERNAL_APPS_prefix + DJANGO_APPS + MY_APPS + EXTERNAL_APPS_suffix


""" Middleware's """
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


""" Template's """
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'apps.core.contexts.profile_image',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


""" Password validation's """
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators


""" Internationalization """
LANGUAGE_CODE = 'en-us'

# Datetime
TIME_ZONE = config("TIME_ZONE", default='Asia/Tehran')
USE_I18N = True
USE_TZ = True

# Translation
LANGUAGES = [
    ('fa', _('Persian')),
    ('en', _('English')),
]
# https://docs.djangoproject.com/en/5.0/topics/i18n/



""" Static files (CSS, JavaScript, Images) """
STATIC_URL = 'static/'
# https://docs.djangoproject.com/en/5.0/howto/static-files/

""" Media files (Video, Image, Gif &...) """
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'

""" Default primary key field type """
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

""" Custom User """
AUTH_USER_MODEL = "users.CustomUser"

""" Backends """
# AUTHENTICATION_BACKENDS = ("apps.users.backends.CustomModelBackend",)


""" Mode Handling """
if DEBUG:
    # Static:
    # STATIC_ROOT = 'static'
    BASE_URL = "*"
    
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]
    
    # Celery:    
    CELERY_BROKER_URL = config("CELERY_BROKER_URL_DEV")
    CELERY_TIMEZONE = TIME_ZONE
    
    # Redis:
    REDIS_HOST = config("REDIS_HOST_dev")
    REDIS_PORT = config("REDIS_PORT_dev")
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    
    # Cache Services:
    # CACHES = {
    #     'default': {
    #         'BACKEND': 'django_redis.cache.RedisCache',
    #         'LOCATION': REDIS_URL,
    #         'OPTIONS': {
    #             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
    #         }
    #     }
    # }
    
    # Email
    EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
    # EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_PORT = config("EMAIL_PORT")
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
    # EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
    # DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
    
    # Development Sqlite3 db:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    # https://docs.djangoproject.com/en/5.0/ref/settings/#databases
    
else:
    STATIC_ROOT = BASE_DIR / 'static'
    
    REDIS_HOST = config("REDIS_HOST_pro")
    REDIS_PORT = config("REDIS_PORT_pro")
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
    
    # Celery:
    CELERY_BROKER_URL = config("CELERY_BROKER_URL_PRO")
    CELERY_TIMEZONE = TIME_ZONE
    
    # Cache Services:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        }
    }
    
    # Email settings
    EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_PORT = config("EMAIL_PORT")
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
    # EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
    # DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
    
    # Production postgresql db:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT"),
        },
    }
    

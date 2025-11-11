import os
from pathlib import Path

BASE_DIR = Path ( __file__ ).resolve ().parent.parent

SECRET_KEY = 'django-insecure-9d@w-h_=g)c47d-zf$b_x&0&r#6aj&aem!mu1!dwmg812z^@13'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'centerapp.apps.CenterappConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'center.urls'

TEMPLATES = [
    {
        'BACKEND' : 'django.template.backends.django.DjangoTemplates',
        'DIRS' : [os.path.join ( BASE_DIR, 'templates' )],
        'APP_DIRS' : True,
        'OPTIONS' : {
            'context_processors' : [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'center.wsgi.application'

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.sqlite3',
        'NAME' : BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME' : 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME' : 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME' : 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME' : 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join ( BASE_DIR, 'media' )
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join ( BASE_DIR, 'static' )
STATICFILES_DIRS = [
    os.path.join ( BASE_DIR, 'centerapp/static' )
]

EMAIL_HOST = 'smtp.ukr.net'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'khayitovkhumoyun000@gmail.com'
EMAIL_HOST_PASSWORD = '24012020'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
"""
Django settings for gdpr_site project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

from .utils import get_env_variable

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    'hvad',
    'django_extensions',
    'compressor',
    'webpack_loader',

    'gdpr'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'gdpr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'gdpr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('GDPR_DATABASE_NAME', default='gdpr'),
        'USER': get_env_variable('GDPR_DATABSE_USERNAME', default=''),
        'PASSWORD': get_env_variable('GDPR_DATABSE_PASSWORD', default=''),
        'HOST': get_env_variable('GDPR_DATABSE_PASSWORD', default='localhost'),
        'PORT': get_env_variable('GDPR_DATABSE_PORT', default=''),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('de', 'German'),
    ('fr', 'French'),
    ('es', 'Spanish'),
    ('it', 'Italian'),
    ('pt', 'Portuguese'),
    ('nl', 'Dutch'),
    ('hr', 'Croatian'),
    ('hu', 'Hungarian'),
    ('ro', 'Romanian'),
    ('et', 'Estonian'),
    ('cs', 'Czech'),
    ('el', 'Greek'),
    ('pl', 'Polish'),
    ('sk', 'Slovak'),
    ('ga', 'Irish'),
    ('fi', 'Finnish'),
    ('sl', 'Slovenian'),
    ('sv', 'Swedish'),
    ('mt', 'Maltese'),
    ('da', 'Danish'),
    ('bg', 'Bulgarian'),
    ('lv', 'Latvian'),
    ('lt', 'Lithuanian')
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

COMPRESS_CSS_FILTERS = [
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(os.path.dirname(BASE_DIR), 'webpack-stats.json'),
    }
}

ALGOLIA = {
    'APPLICATION_ID': get_env_variable('GDPR_ALGOLIA_APPLICATION_ID', default=None),
    'API_KEY':  get_env_variable('GDPR_ALGOLIA_API_KEY', default=None)
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}

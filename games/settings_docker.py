"""
Django settings for games project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os

import dj_database_url
import environ
from pathlib import Path

from decouple import config

env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str, "w((&w@u3!)2$75uhxnk3x68bykks&=gn0$r@k^reqfuvc*8bp2"),
    AWS_ACCESS_KEY=(str, "AKIAJM5VET276RQ3UYPA"),
    AWS_SECRET_KEY=(str, "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"),
    ALLOWED_HOSTS=(str, "*"),
    CORS_ORIGIN_WHITELIST=(str, "http://localhost:3333,http://127.0.0.1:3333,http://localhost:3000"),
    REDIS_URL=(str, "redis://127.0.0.1:6379"),
    USE_S3=(bool, False),
    MEDIA_VIDEO_CDN_URL=(str, "d1f2porn8aqwt0.cloudfront.net"),
    MEDIA_CDN_URL=(str, "d1i4l9sy6nvjes.cloudfront.net"),
    RECAPTCHA_KEY=(str, "6LcWGtMZAAAAAKYSjxQvsRx2MH0V1bnhNsx9GllI"),
    ADMIN_URL=(str, "admin"),
    USE_POSTGRES=(bool, False),
    POSTGRES_IP=(str, "127.0.0.1"),
    DB_PASSWORD=(str, ""),
    DB_NAME=(str, ""),
    DB_USER=(str, ""),
    ONVOPAY_API_KEY = (str, "onvo_test_secret_key_IK7klm_16d2DcK6SBn95b_HEw41WSh8vZQ8d9ttoZE_vWXPfcvlGL2jVyY6lK90-htxVpQ_Uw5XGNmGDdvrPLg"),
    RECAPTCHA_SECRET = (str, "6Ldv3-wqAAAAAFW8WPmD6dtmyB5aeLG2P_DeM8if"),
    ONLINE_PAYMENT = (bool, False)
)
environ.Env.read_env()
USE_POSTGRES = env("USE_POSTGRES")
DB_NAME = env("DB_NAME")
DB_USER = env("DB_USER")
DB_PASSWORD = env("DB_PASSWORD")
POSTGRES_IP = env("POSTGRES_IP")
ONVOPAY_API_KEY = env('ONVOPAY_API_KEY')
ONLINE_PAYMENT = env('ONLINE_PAYMENT')
BUSINESSES = ("Ready Games", "Marisqueria Leiva")
RECAPTCHA_SECRET_KEY = env("RECAPTCHA_SECRET")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)0nm0komohtrna_tfhhaq(#_cb!h)ob8ip8wz5jm&y8=p^5pyc'

DEBUG = True

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

CORS_ALLOWED_ORIGINS = [
    "https://readygamescr.com",
    "https://www.readygamescr.com",
    "http://localhost:3000",
    "https://ready-games-ui.vercel.app",
    "https://readygames.vercel.app",
    "http://localhost:5173"
]

CSRF_TRUSTED_ORIGINS = [
    "https://readygamescr.com",
    "https://www.readygamescr.com",
    "http://localhost:8000",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'babel',
    'shortuuid',
    'openpyxl'
]

# Custom apps
INSTALLED_APPS += [
    "product",
    "ui",
    "administration",
    "possimplified"
]

# Third-party apps
INSTALLED_APPS += [
    "rest_framework",
    "colorfield",
    "storages"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'games.middleware.WwwRedirectMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}


ROOT_URLCONF = 'games.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates")
        ],
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

WSGI_APPLICATION = 'games.wsgi.application'

if USE_POSTGRES:
    DATABASES = {
        'default': {

            'ENGINE': 'django.db.backends.postgresql_psycopg2',

            'NAME': DB_NAME,

            'USER': DB_USER,

            'PASSWORD': DB_PASSWORD,

            'HOST': POSTGRES_IP,

            'PORT': 5432,

            }
    }

else:
    # When running locally in development or in CI, a sqlite database file will be used instead
    # to simplify initial setup. Longer term it's recommended to use Postgres locally too.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "America/Costa_Rica"

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'collected-static'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'collected-media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGS_LIMIT = 5000

S3_ENABLED = config('S3_ENABLED', cast=bool, default=False)
LOCAL_SERVE_MEDIA_FILES = config('LOCAL_SERVE_MEDIA_FILES', cast=bool, default=not S3_ENABLED)
LOCAL_SERVE_STATIC_FILES = config('LOCAL_SERVE_STATIC_FILES', cast=bool, default=not S3_ENABLED)

if (not LOCAL_SERVE_MEDIA_FILES or not LOCAL_SERVE_STATIC_FILES) and not S3_ENABLED:
    raise ValueError('S3_ENABLED must be true if either media or static files are not served locally')

STATIC_LOCATION = None
STATIC_DEFAULT_ACL = None
PUBLIC_MEDIA_LOCATION = None
PUBLIC_MEDIA_DEFAULT_ACL = None
PRIVATE_MEDIA_LOCATION = None
PRIVATE_MEDIA_DEFAULT_ACL = None

if S3_ENABLED:
    AWS_ACCESS_KEY_ID = config('BUCKETEER_AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('BUCKETEER_AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('BUCKETEER_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('BUCKETEER_AWS_REGION')
    AWS_DEFAULT_ACL = None
    AWS_S3_SIGNATURE_VERSION = config('S3_SIGNATURE_VERSION', default='s3v4')
    AWS_S3_ENDPOINT_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    if not LOCAL_SERVE_STATIC_FILES:
        STATIC_DEFAULT_ACL = 'public-read'
        STATIC_LOCATION = 'static'
        STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/{STATIC_LOCATION}/'
        STATICFILES_STORAGE = 'games.utils.storage_backends.StaticStorage'

    if not LOCAL_SERVE_MEDIA_FILES:
        PUBLIC_MEDIA_DEFAULT_ACL = 'public-read'
        PUBLIC_MEDIA_LOCATION = 'media/public'

        MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/'
        DEFAULT_FILE_STORAGE = 'games.utils.storage_backends.PublicMediaStorage'

        PRIVATE_MEDIA_DEFAULT_ACL = 'private'
        PRIVATE_MEDIA_LOCATION = 'media/private'
        PRIVATE_FILE_STORAGE = 'games.utils.storage_backends.PrivateMediaStorage'


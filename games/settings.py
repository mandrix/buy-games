"""
Django settings for games project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import environ
from pathlib import Path


env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str, "w((&w@u3!)2$75uhxnk3x68bykks&=gn0$r@k^reqfuvc*8bp2"),
    AWS_ACCESS_KEY=(str, "AKIAJM5VET276RQ3UYPA"),
    AWS_SECRET_KEY=(str, "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"),
    ALLOWED_HOSTS=(str, "*"),
    CORS_ORIGIN_WHITELIST=(str, "http://localhost:3333,http://127.0.0.1:3333"),
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
)
environ.Env.read_env()
USE_POSTGRES = env("USE_POSTGRES")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)0nm0komohtrna_tfhhaq(#_cb!h)ob8ip8wz5jm&y8=p^5pyc'

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

CORS_ALLOWED_ORIGINS = [
    "https://buy-games.herokuapp.com",
    "http://localhost:3000",
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders'
]

# Custom apps
INSTALLED_APPS += [
    "product",
]

# Third-party apps
INSTALLED_APPS += [
    "rest_framework",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'games.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if USE_POSTGRES:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': env("POSTGRES_IP"),
            'PORT': '5432',
        }
    }
else:
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# settings.py

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

try:
    if django_heroku := __import__("django_heroku"):
        django_heroku.settings(locals())
except ModuleNotFoundError:
    pass

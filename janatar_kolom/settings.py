"""
Django settings for indianconsumersofficial project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from janatar_kolom.environment_test import getPlatform

platform = getPlatform()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8lc+^vcchig*vmc*3x+g(v8cha7$ofwli(jo%urhw(kj+d9w=j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
if platform == "Production":
    DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '192.168.1.5', '192.168.43.43', '192.168.43.100', 'localhost', 'janatarkalam.herokuapp.com', 'janatarkalam.com', 'www.janatarkalam.com', '139.59.25.167']


# Application definition

INSTALLED_APPS = [
    'authentication',
    'customer',
    'website',
    'administrator',
    'organisation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'janatar_kolom.urls'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
     'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

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

WSGI_APPLICATION = 'janatar_kolom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if platform == "Production":
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': "dfb3s2o2dp9dit",
    #         'USER': "malzuojheeqbyk",
    #         'PASSWORD': "f2dd5ea52ca33088ac42d72f93b7df7aebea061ab370f0165128c642d9bc0e91",
    #         'HOST': "ec2-174-129-32-215.compute-1.amazonaws.com",
    #         'PORT': "5432"
    #     }
    # }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': "janatarkalam-website",
            'USER': "doadmin",
            'PASSWORD': "AVNS_k1AbkM-a773xGRh",
            'HOST': "news-provider-cluster-do-user-4837440-0.b.db.ondigitalocean.com",
            'PORT': "25060"
        }
    }
else:
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': "janatar_kolom",
    #         'USER': "postgres",
    #         'PASSWORD': "pass1234",
    #         'HOST': "localhost",
    #         'PORT': "5432"
    #     }
    # }
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': "dfb3s2o2dp9dit",
    #         'USER': "malzuojheeqbyk",
    #         'PASSWORD': "f2dd5ea52ca33088ac42d72f93b7df7aebea061ab370f0165128c642d9bc0e91",
    #         'HOST': "ec2-174-129-32-215.compute-1.amazonaws.com",
    #         'PORT': "5432"
    #     }
    # }DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': "dfb3s2o2dp9dit",
    #         'USER': "malzuojheeqbyk",
    #         'PASSWORD': "f2dd5ea52ca33088ac42d72f93b7df7aebea061ab370f0165128c642d9bc0e91",
    #         'HOST': "ec2-174-129-32-215.compute-1.amazonaws.com",
    #         'PORT': "5432"
    #     }
    # }

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': "janatarkalam",
            'USER': "gourab",
            'PASSWORD': "pass1234",
            'HOST': "postgresql-75775-0.cloudclusters.net",
            'PORT': "18225"
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
AUTH_USER_MODEL = 'authentication.User'

# CLOUDINARY = {
#     'cloud_name': 'janatarkalam',
#     'api_key': '158518893827718',
#     'api_secret': 'TPhvUo9kxFVeETYmSKvMCYlXMLc'
# }
#
# CLOUDINARY_APP_NAME = "janatarkalam"
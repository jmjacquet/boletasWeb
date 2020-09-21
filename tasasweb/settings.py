# -*- coding: utf-8 -*-
import os
from decouple import config
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [    
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',  
    'django.contrib.humanize',
    'tadese',    
    'bootstrap3',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tasasweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                    os.path.join(BASE_DIR, 'templates'),
                ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "staticfiles"),   
)

STATICFILES_FINDERS = [
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]



WSGI_APPLICATION = 'tasasweb.wsgi.application'


MUNI_ID = os.environ.get("MUNI_ID", "000")
MUNI_DB = os.environ.get("MUNI_DB", "")
MUNI_DIR = os.environ.get("MUNI_DIR", "")
DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': MUNI_DB,           # Or path to database file if using sqlite3.
        'USER': DB_USER,                      # Not used with sqlite3.
        'PASSWORD': DB_PASS,            # Not used with sqlite3.
        'HOST': 'www.boletaweb.com.ar',                   # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default.
        'OPTIONS':{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    },
}



# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es-AR'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_THOUSAND_SEPARATOR = True
USE_L10N = True
USE_TZ = True
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
TIME_INPUT_FORMATS = ('%H:%M',)
DATE_INPUT_FORMATS = ('%d/%m/%Y',)
DATE_FORMATS = ('%d/%m/%Y',)
TIME_FORMATS = ('%H:%M',)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT = '/home/grupogua/webapps/ironweb/ggcontable/staticfiles'
STATIC_URL = '/static/'
DIR_MUNIS = os.path.join(STATIC_URL,'munis',MUNI_DIR)


ROOT_URL = '/'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL='/'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend','tadese.authentication.ContribuyentesBackend','tadese.authentication.EstudiosBackend','tadese.authentication.idCuotaBackend')

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_NAME = config('SESSION_COOKIE_NAME', default='')
SESSION_COOKIE_AGE = 86400
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'




from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger',} 


CRISPY_TEMPLATE_PACK = 'bootstrap3'           

INTERNAL_IPS = [    
    '127.0.0.1',    
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = 'errores_web@grupoguadalupe.com.ar'
DEFAULT_FROM_EMAIL = 'errores_web@grupoguadalupe.com.ar'

EMAIL_USE_TLS = True
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')

LOGGING = {
   'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
         'require_debug_false': {
             '()': 'django.utils.log.RequireDebugFalse'
         }
     },
    'handlers': {
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR, "errores.log"),
            'formatter': 'verbose'
        },
         'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'filters': ['require_debug_false'],
             # But the emails are plain text by default - HTML is nicer
            'include_html': True,
            'formatter': 'verbose',
        },
         'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
        
        'tadese': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'xhtml2pdf': {
            'handlers': ['console'],
            'level': 'DEBUG'
       },
    }
}


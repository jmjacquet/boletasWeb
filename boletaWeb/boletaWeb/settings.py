# -*- coding: utf-8 -*-
# Django settings for sistema_bomberos project.

import os
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..') #every dot represent the location of the folder so when you try to delete one dot, the path will be change

SITE_ROOT = PROJECT_ROOT

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
       ('JuanMa', 'errores_web@grupoguadalupe.com.ar'),
)

MANAGERS = ADMINS

#Traigo los datos de configuracion del Apache

MUNI_ID = os.environ['MUNI_ID']
MUNI_DB = os.environ['MUNI_DB']
MUNI_DIR = os.environ['MUNI_DIR']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': MUNI_DB,           # Or path to database file if using sqlite3.
        'USER': 'gg',                      # Not used with sqlite3.
        'PASSWORD': 'battlehome',            # Not used with sqlite3.
        'HOST': 'www.boletaweb.com.ar',                   # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default.
    },
}


ALLOWED_HOSTS = '*'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

LANGUAGE_CODE = 'es-AR'

SITE_ID = 1

USE_I18N = False

USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'

MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# MEDIA_ROOT = '/home/grupogua/webapps/boletadjango/boletaWeb/media'

MEDIA_URL = '/media/'

STATIC_PATH = '/home/grupogua/webapps/boletadjstatic/'

STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
# STATIC_ROOT = '/home/grupogua/webapps/boletadjango/boletaWeb/staticfiles'

STATIC_URL = '/staticfiles/'

DIR_MUNIS = os.path.join(STATIC_URL,'munis',MUNI_DIR)

STATICFILES_DIRS = (
   os.path.join(SITE_ROOT, 'staticfiles'),

)

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)
ADMIN_MEDIA_PREFIX = os.path.join(SITE_ROOT, 'static/admin/')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_CONTEXT_PROCESSORS =   (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

SECRET_KEY = 'ydr+)juyj)d(r(h-9mls-rs3ax11_70#&9dcl^ec-o17aa(z81'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
       'debug_toolbar.middleware.DebugToolbarMiddleware',#Barra DEBUG
)

ROOT_URLCONF = 'boletaWeb.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'boletaWeb.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'tadese',
    #'debug_toolbar',
    'bootstrap3',
    'django_extensions',
)


EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'grupogua_errores'
EMAIL_HOST_PASSWORD = 'qwerty'
SERVER_EMAIL = 'errores_web@grupoguadalupe.com.ar'
DEFAULT_FROM_EMAIL = 'errores_web@grupoguadalupe.com.ar'
SESSION_COOKIE_NAME = "tadese"
SECRET_KEY='grupoguadalupe'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_NAME = "grupogua"
SESSION_COOKIE_AGE = 86400
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
            'filename': os.path.join(SITE_ROOT, "errores.log"),
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
    }
}

ROOT_URL = '/'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL='/'
CRISPY_TEMPLATE_PACK = 'bootstrap3'
AUTH_PROFILE_MODULE = 'tadese.UserProfile'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend','tadese.authentication.ContribuyentesBackend','tadese.authentication.EstudiosBackend','tadese.authentication.idCuotaBackend')
#AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend','tadese.authentication.ContribuyentesBackend')

BOOTSTRAP3 = {

    # The Bootstrap base URL
    'base_url': os.path.join(SITE_ROOT, 'staticfiles/css/'),

    # The complete URL to the Bootstrap CSS file (None means derive it from base_url)
    'css_url': None,

    # The complete URL to the Bootstrap CSS file (None means no theme)
    'theme_url': None,

    # The complete URL to the Bootstrap JavaScript file (None means derive it from base_url)
    'javascript_url': None,

    # Put JavaScript in the HEAD section of the HTML document (only relevant if you use bootstrap3.html)
    'javascript_in_head': False,

    # Include jQuery with Bootstrap JavaScript (affects django-bootstrap3 template tags)
    'include_jquery': False,

    # Label class to use in horizontal forms
    'horizontal_label_class': 'col-md-2',

    # Field class to use in horizontal forms
    'horizontal_field_class': 'col-md-5',

    # Set HTML required attribute on required fields
    'set_required': True,

    # Set HTML disabled attribute on disabled fields
    'set_disabled': False,

    # Set placeholder attributes to label if no placeholder is provided
    'set_placeholder': True,

    # Class to indicate required (better to set this in your Django form)
    'required_css_class': '',

    # Class to indicate error (better to set this in your Django form)
    'error_css_class': 'has-error',

    # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
    'success_css_class': 'has-success',
}


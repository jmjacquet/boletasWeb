# -*- coding: utf-8 -*-
from .settings import *
import os

DEBUG = True
# DEBUG = False

TEMPLATE_DEBUG = DEBUG

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.environ.get('ENTIDAD_DB'),           # Or path to database file if using sqlite3.
            'USER':  'gg',    
            'PASSWORD':  'battlehome',            # Not used with sqlite3.
            'HOST':  '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',      
        },
    }

import sys
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
if TESTING: #Covers regular testing and django-coverage
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', #
            'NAME': 'test.db', # Ruta al archivo de la base de datos
            }
        }

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',#Barra DEBUG    
]

INSTALLED_APPS += [
    'rest_framework',
    'rest_framework.authtoken',        
    'rest_framework_swagger',
    'corsheaders',
    'api',
    'debug_toolbar',        
]



CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DATE_FORMAT': '%d/%m/%Y',
    'DATETIME_FORMAT': '%d/%m/%Y %H:%M:%S',    
    'DATE_INPUT_FORMATS': ['%d/%m/%Y'],
    
}


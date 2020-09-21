# -*- coding: utf-8 -*-
from .settings import *


DEBUG = True
# DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': MUNI_DB,           # Or path to database file if using sqlite3.
        'USER': 'gg',                      # Not used with sqlite3.
        'PASSWORD': 'battlehome',            # Not used with sqlite3.
        'HOST': 'localhost',                   # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3308',                      # Set to empty string for default.
        'OPTIONS':{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
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


SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "apps.api.inspectors.SwaggerAutoSchema"
}


# REST_USE_JWT = True

# import datetime
# # JWT settings
# JWT_AUTH = {
#     'JWT_ENCODE_HANDLER':
#     'rest_framework_jwt.utils.jwt_encode_handler',
 
#     'JWT_DECODE_HANDLER':
#     'rest_framework_jwt.utils.jwt_decode_handler',
 
#     'JWT_PAYLOAD_HANDLER':
#     'rest_framework_jwt.utils.jwt_payload_handler',
 
#     'JWT_PAYLOAD_GET_USER_ID_HANDLER':
#     'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
 
#     'JWT_RESPONSE_PAYLOAD_HANDLER':
#     'rest_framework_jwt.utils.jwt_response_payload_handler',
 
#     'JWT_SECRET_KEY': SECRET_KEY,
#     'JWT_GET_USER_SECRET_KEY': None,
#     'JWT_PUBLIC_KEY': None,
#     'JWT_PRIVATE_KEY': None,
#     'JWT_ALGORITHM': 'HS256',
#     'JWT_VERIFY': True,
#     'JWT_VERIFY_EXPIRATION': True,
#     'JWT_LEEWAY': 0,
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3000),
#     'JWT_AUDIENCE': None,
#     'JWT_ISSUER': None, 
#     'JWT_ALLOW_REFRESH': False,
#     'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
#     'JWT_AUTH_HEADER_PREFIX': 'GG',
#     'JWT_AUTH_COOKIE': None,
# }

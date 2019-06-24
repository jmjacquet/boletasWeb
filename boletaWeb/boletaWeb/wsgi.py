import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

sys.path.append(PROJECT_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'boletaWeb.settings'


import django.core.handlers.wsgi


_application = django.core.handlers.wsgi.WSGIHandler()


def application(environ, start_response):
  os.environ['MUNI_ID'] = environ['MUNI_ID']
  os.environ['MUNI_DB'] = environ['MUNI_DB']
  os.environ['MUNI_DIR'] = environ['MUNI_DIR']
  return _application(environ, start_response)

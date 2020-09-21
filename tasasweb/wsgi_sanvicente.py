import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

sys.path.append(PROJECT_DIR)

from django.core.wsgi import get_wsgi_application


def application(environ, start_response):
  os.environ['DJANGO_SETTINGS_MODULE'] = 'tasasweb.production'
  os.environ["MUNI_ID"] = '545'
  os.environ["MUNI_DB"] = 'gg_sanvicente'
  os.environ["MUNI_DIR"] = 'sanvicente'
  _application = get_wsgi_application()
  return _application(environ, start_response)
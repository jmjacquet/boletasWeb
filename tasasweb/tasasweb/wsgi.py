import os
import sys

from django.core.wsgi import get_wsgi_application


def application(environ, start_response):
  os.environ['DJANGO_SETTINGS_MODULE'] = 'tasasweb.production'
  os.environ["MUNI_ID"] = environ.get("MUNI_ID", "000")
  os.environ["MUNI_DB"] = environ.get("MUNI_DB", "gg_prueba")
  os.environ["MUNI_DIR"] = environ.get("MUNI_DIR", "prueba")     
  os.environ['MUNI_DB_PASSWD'] = 'battlehome'
  os.environ['ERROR_MAIL_USER'] = 'grupogua_errores'
  os.environ['ERROR_MAIL_PASSWD'] = 'Sarasa1616'
  _application = get_wsgi_application()
  return _application(environ, start_response)
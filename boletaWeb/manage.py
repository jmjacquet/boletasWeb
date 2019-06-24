#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boletaWeb.settings")
    os.environ['MUNI_ID'] = '947'
    os.environ['MUNI_DB'] = 'gg_rufino'
    os.environ['MUNI_DIR'] = 'prueba'
    
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasasweb.development")
    try:
        # os.environ["MUNI_ID"] = '545'
        # os.environ["MUNI_DB"] = 'gg_sanvicente'        
        os.environ['MUNI_ID'] = '000'
        os.environ['MUNI_DB'] = 'gg_prueba'
        os.environ['MUNI_DIR'] = 'prueba'        
        from django.core.management import execute_from_command_line
    except ImportError:
        
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)

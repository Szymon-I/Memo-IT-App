"""
WSGI config for memoit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memoit.settings')

# application = get_wsgi_application()


import os
import sys
import django
from django.core.handlers.wsgi import WSGIHandler

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

os.environ["DJANGO_SETTINGS_MODULE"] = "memoit.settings"

django.setup()

application = WSGIHandler()

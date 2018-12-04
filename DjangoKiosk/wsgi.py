"""
WSGI config for DjangoKiosk project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""
import os,sys

from django.core.wsgi import get_wsgi_application

sys.path.append(r'C:\Users\red.cheng\Documents\GitHub\DjangoKiosk\DjangoKiosk')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoKiosk.settings")

application = get_wsgi_application()

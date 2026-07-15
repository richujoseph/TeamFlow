"""
TeamFlow EPMS — WSGI Configuration.

Exposes the WSGI callable as a module-level variable named ``application``.
Used by WSGI servers (e.g., Gunicorn) for synchronous request handling.

https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

application = get_wsgi_application()

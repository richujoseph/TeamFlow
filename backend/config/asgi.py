"""
TeamFlow EPMS — ASGI Configuration.

Exposes the ASGI callable as a module-level variable named ``application``.
Used by ASGI servers (e.g., Daphne, Uvicorn) for async request handling.

https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

application = get_asgi_application()

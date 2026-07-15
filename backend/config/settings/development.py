from .base import *
from .base import env

DEBUG = True
CORS_ALLOW_ALL_ORIGINS = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
JWT_SETTINGS["COOKIE_SECURE"] = False
try:
    import django_extensions

    INSTALLED_APPS += ["django_extensions"]
except ImportError:
    pass
LOGGING["root"]["level"] = "DEBUG"
LOGGING["loggers"]["django"]["level"] = "INFO"
LOGGING["loggers"]["apps"]["level"] = "DEBUG"

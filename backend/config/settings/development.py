"""
TeamFlow EPMS — Development Settings.

Inherits from base settings and applies local development overrides:
- DEBUG mode enabled
- Relaxed CORS (allow all origins)
- Console email backend
- Non-secure JWT cookies (HTTP allowed)
- Verbose logging
"""

from .base import *  # noqa: F401, F403
from .base import env

# ---------------------------------------------------------------------------
# Debug
# ---------------------------------------------------------------------------
DEBUG = True

# ---------------------------------------------------------------------------
# CORS — allow all origins in development
# ---------------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True

# ---------------------------------------------------------------------------
# Email — output to console instead of sending
# ---------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ---------------------------------------------------------------------------
# JWT Cookies — allow over HTTP in development
# ---------------------------------------------------------------------------
JWT_SETTINGS["COOKIE_SECURE"] = False  # noqa: F405

# ---------------------------------------------------------------------------
# Additional dev tools
# ---------------------------------------------------------------------------
try:
    import django_extensions  # noqa: F401

    INSTALLED_APPS += ["django_extensions"]  # noqa: F405
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Logging — verbose output for development
# ---------------------------------------------------------------------------
LOGGING["root"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["django"]["level"] = "INFO"  # noqa: F405
LOGGING["loggers"]["apps"]["level"] = "DEBUG"  # noqa: F405

"""
TeamFlow EPMS — Production Settings.

Inherits from base settings and applies production-hardened overrides:
- DEBUG disabled
- Strict CORS whitelist
- HTTPS enforcement (HSTS, SSL redirect, secure cookies)
- WhiteNoise for static file serving
- Sentry error tracking
"""

from .base import *  # noqa: F401, F403
from .base import env

# ---------------------------------------------------------------------------
# Debug — NEVER enable in production
# ---------------------------------------------------------------------------
DEBUG = False

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ---------------------------------------------------------------------------
# CORS — strict whitelist
# ---------------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=["https://teamflow.example.com"],
)

# ---------------------------------------------------------------------------
# JWT Cookies — HTTPS only in production
# ---------------------------------------------------------------------------
JWT_SETTINGS["COOKIE_SECURE"] = True  # noqa: F405
JWT_SETTINGS["COOKIE_SAMESITE"] = "Lax"  # noqa: F405

# ---------------------------------------------------------------------------
# Static Files — WhiteNoise
# ---------------------------------------------------------------------------
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa: F405
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ---------------------------------------------------------------------------
# Email — configure real SMTP in production
# ---------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="smtp.example.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)

# ---------------------------------------------------------------------------
# Sentry — error tracking
# ---------------------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN", default="")
if SENTRY_DSN:
    import sentry_sdk

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
        environment="production",
    )

# ---------------------------------------------------------------------------
# Logging — structured for production log aggregation
# ---------------------------------------------------------------------------
LOGGING["root"]["level"] = "WARNING"  # noqa: F405
LOGGING["loggers"]["django"]["level"] = "WARNING"  # noqa: F405
LOGGING["loggers"]["apps"]["level"] = "INFO"  # noqa: F405

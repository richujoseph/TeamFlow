"""
TeamFlow EPMS — Base Settings.

Shared settings for ALL environments. Environment-specific settings
(development.py, production.py) inherit from this module and override
as needed.

Configuration is loaded from environment variables using django-environ.
"""

import os
from pathlib import Path

import environ

# ---------------------------------------------------------------------------
# Path Configuration
# ---------------------------------------------------------------------------
# BASE_DIR points to the backend/ directory (parent of config/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize django-environ — reads from .env file in project root
env = environ.Env(
    DEBUG=(bool, False),
    DJANGO_ENV=(str, "development"),
)

# Read .env file from the teamflow root (one level above backend/)
ENV_FILE = BASE_DIR.parent / ".env"
if ENV_FILE.exists():
    environ.Env.read_env(str(ENV_FILE))

# ---------------------------------------------------------------------------
# Core Settings
# ---------------------------------------------------------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY", default="insecure-dev-key-change-in-production")

DEBUG = env("DEBUG", default=False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# ---------------------------------------------------------------------------
# Application Definition
# ---------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
]

TEAMFLOW_APPS = [
    "apps.accounts",
    "apps.organizations",
    "apps.projects",
    "apps.teams",
    "apps.tasks",
    "apps.meetings",
    "apps.reports",
    "apps.notifications",
    "apps.audit",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + TEAMFLOW_APPS

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------------------------------------------------
# URL Configuration
# ---------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------------------------------------------------------------------------
# WSGI / ASGI
# ---------------------------------------------------------------------------
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ---------------------------------------------------------------------------
# Database — PostgreSQL via environment variables
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="teamflow"),
        "USER": env("POSTGRES_USER", default="teamflow"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="teamflow_dev_password"),
        "HOST": env("POSTGRES_HOST", default="localhost"),
        "PORT": env.int("POSTGRES_PORT", default=5432),
        "OPTIONS": {
            "connect_timeout": 5,
        },
    }
}

# Use BigAutoField as default primary key type (our models use UUID,
# but Django internals and third-party apps may need this).
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Custom User Model
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"

# ---------------------------------------------------------------------------
# Password Validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static Files
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# ---------------------------------------------------------------------------
# Media Files
# ---------------------------------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------------------------
# Redis Cache
# ---------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://localhost:6379/0"),
    }
}

# ---------------------------------------------------------------------------
# Session — use cache-backed sessions for performance
# ---------------------------------------------------------------------------
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# ---------------------------------------------------------------------------
# CORS — base config (overridden per environment)
# ---------------------------------------------------------------------------
CORS_ALLOW_CREDENTIALS = True  # Required for cookie-based auth

# ---------------------------------------------------------------------------
# JWT Cookie Settings
# ---------------------------------------------------------------------------
JWT_SETTINGS = {
    "SECRET_KEY": env("JWT_SECRET_KEY", default=SECRET_KEY),
    "ACCESS_TOKEN_LIFETIME_MINUTES": env.int(
        "JWT_ACCESS_TOKEN_LIFETIME_MINUTES", default=30
    ),
    "REFRESH_TOKEN_LIFETIME_DAYS": env.int(
        "JWT_REFRESH_TOKEN_LIFETIME_DAYS", default=7
    ),
    "COOKIE_SECURE": env.bool("JWT_COOKIE_SECURE", default=False),
    "COOKIE_HTTPONLY": env.bool("JWT_COOKIE_HTTPONLY", default=True),
    "COOKIE_SAMESITE": env("JWT_COOKIE_SAMESITE", default="Lax"),
    "ACCESS_COOKIE_NAME": "teamflow_access",
    "REFRESH_COOKIE_NAME": "teamflow_refresh",
}

# ---------------------------------------------------------------------------
# Celery Configuration (stub — worker deferred to Phase 2)
# ---------------------------------------------------------------------------
CELERY_BROKER_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

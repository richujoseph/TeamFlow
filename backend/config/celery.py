"""
TeamFlow EPMS — Celery Configuration (Stub).

This module configures the Celery application for asynchronous task processing.
The actual Celery worker container is deferred to Phase 2 — this file exists
so that tasks can be defined in apps without import errors.

Usage (Phase 2+):
    celery -A config worker --loglevel=info
"""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("teamflow")

# Load Celery settings from Django settings, using the CELERY_ namespace.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for verifying Celery connectivity."""
    print(f"Request: {self.request!r}")

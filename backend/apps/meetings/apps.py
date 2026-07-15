"""
TeamFlow EPMS — Meetings App Configuration.
"""

from django.apps import AppConfig


class MeetingsConfig(AppConfig):
    """Configuration for the meetings app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.meetings"
    label = "meetings"
    verbose_name = "Meetings"

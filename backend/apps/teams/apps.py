"""
TeamFlow EPMS — Teams App Configuration.
"""

from django.apps import AppConfig


class TeamsConfig(AppConfig):
    """Configuration for the teams app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.teams"
    label = "teams"
    verbose_name = "Teams"

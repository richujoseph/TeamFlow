"""
TeamFlow EPMS — Organizations App Configuration.
"""

from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    """Configuration for the organizations app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.organizations"
    label = "organizations"
    verbose_name = "Organizations"

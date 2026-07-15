"""
TeamFlow EPMS — Reports App Configuration.
"""

from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """Configuration for the reports app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.reports"
    label = "reports"
    verbose_name = "Reports"

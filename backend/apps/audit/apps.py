"""
TeamFlow EPMS — Audit App Configuration.
"""

from django.apps import AppConfig


class AuditConfig(AppConfig):
    """Configuration for the audit app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.audit"
    label = "audit"
    verbose_name = "Audit"

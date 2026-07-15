"""
TeamFlow EPMS — Projects App Configuration.
"""

from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    """Configuration for the projects app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.projects"
    label = "projects"
    verbose_name = "Projects"

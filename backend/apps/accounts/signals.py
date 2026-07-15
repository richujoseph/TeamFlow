"""
TeamFlow EPMS — Accounts Signals.

Auto-creates a UserProfile whenever a new User is created.
This ensures every user always has an associated profile record.

Connected in AccountsConfig.ready() to avoid circular imports.
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender="accounts.User")
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile automatically when a new User is saved.

    Only triggers on initial creation (created=True), not updates.
    Uses get_or_create to be idempotent — safe to call multiple times.
    """
    if created:
        from apps.accounts.models import UserProfile

        profile, was_created = UserProfile.objects.get_or_create(user=instance)
        if was_created:
            logger.info("Created profile for user: %s", instance.email)

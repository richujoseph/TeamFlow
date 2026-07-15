import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender="accounts.User")
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        from apps.accounts.models import UserProfile

        profile, was_created = UserProfile.objects.get_or_create(user=instance)
        if was_created:
            logger.info("Created profile for user: %s", instance.email)

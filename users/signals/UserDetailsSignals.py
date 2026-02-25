from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
from users.models import UserDetails

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_details(sender, instance, created, **kwargs):
    """
    Automatically create UserDetails when a User is created
    """
    if created:
        UserDetails.objects.get_or_create(user=instance)

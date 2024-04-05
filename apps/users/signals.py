from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile


@receiver(post_save, sender=CustomUser)
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Profile.objects.create(
            user=user,
            nick_name=user.username,
            is_active=False,
        )


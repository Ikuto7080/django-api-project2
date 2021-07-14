from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Account


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_delete, sender=Account)
def pre_delete_account(sender, instance, **kwargs):
    user = User.objects.get(id=instance.user_id)
    user.delete()



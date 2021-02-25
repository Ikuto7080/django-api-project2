from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fb_token = models.CharField(max_length=1000)
    ig_token = models.CharField(max_length=1000)
    fb_id = models.CharField(max_length=30, unique=True)
    ig_id = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return str(self.id)



class FbPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_url = models.URLField(max_length=1000)

    def __str__(self):
        return str(self.id)

class IgPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media_url = models.URLField(max_length=1000)

    def __str__(self):
        return str(self.id) 


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)







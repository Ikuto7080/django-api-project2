from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    boi = models.TextField(default='no bio...', blank=True, null=True)
    friends = models.ManyToManyField(User, related_name="friends", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def __str__(self):
        return str(self.user)

STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    fb_token = models.CharField(max_length=1000, blank=True)
    ig_token = models.CharField(max_length=1000)
    fb_id = models.CharField(max_length=30, unique=True, blank=True)
    ig_id = models.CharField(max_length=30, unique=True)
    line_user_id = models.CharField(max_length=100, null=True)


    def __str__(self):
        return str(self.id)

class ALLPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media_url = models.URLField(max_length=1000)
    post_url = models.URLField(max_length=1000)
    message = models.URLField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    location_name = models.CharField(max_length=100)
    fb_permalink = models.URLField(max_length=1000)
    ig_permalink = models.URLField(max_length=1000)
    image = models.ImageField(null=True, blank=1000, upload_to='allposts/')
    google_info = models.JSONField(null=True, blank=True)
    place_id = models.CharField(max_length=1000)
    location_id = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.id)


class GooglePlace(models.Model):
    info = models.JSONField(null=True, blank=True)
    place_id = models.CharField(max_length=1000)
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        return self.info['name'] if self.info else self.place_id
        


class IgLocation(models.Model):
    ig_id = models.CharField(max_length=1000)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    google_place = models.ForeignKey(GooglePlace, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=50, choices=[('facebook', 'Facebook'),('instagram', 'Instagram')])
    permalink = models.URLField(max_length=1000)
    message = models.CharField(max_length=1000, null=True, blank=True)
    ig_id = models.CharField(max_length=1000)


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.URLField(max_length=1000, null=True, blank=True)
    image = models.ImageField(null=True, blank=1000, upload_to='postimage/')

    


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)













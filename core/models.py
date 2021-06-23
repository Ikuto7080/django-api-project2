from django.db import models
from django.contrib.auth.models import User
import requests
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


    def __str__(self):
        return str(self.user)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fb_token = models.CharField(max_length=1000, null=True, blank=True)
    ig_token = models.CharField(max_length=1000, null=True, blank=True)
    fb_id = models.CharField(max_length=30, unique=True, null=True, blank=True)
    ig_id = models.CharField(max_length=30, null=True, blank=True)
    #line_user_id = models.CharField(max_length=100, null=True)
    profile_picture = models.URLField(max_length=1000, blank=True)
    inviter = models.OneToOneField("Account", null=True, blank=True, on_delete=models.SET_NULL)



    def __str__(self):
        return str(self.id)


class Device(models.Model):
    account = models.OneToOneField("Account", on_delete=models.CASCADE)
    fcm_token = models.CharField(max_length=1000, null=True, blank=True)


class GooglePlace(models.Model):
    info = models.JSONField(null=True, blank=True)
    place_id = models.CharField(max_length=1000)
    latitude = models.FloatField()
    longitude = models.FloatField()
    hidden = models.BooleanField(default=False)
    def __str__(self):
        return self.info['name'] if self.info else self.place_id



class IgLocation(models.Model):
    ig_id = models.CharField(max_length=1000)

class FoursquareVenue(models.Model):
    venue_id = models.CharField(max_length=100, unique=True)
    data = models.JSONField()

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foursquare = models.ForeignKey(FoursquareVenue, on_delete=models.CASCADE, null=True, blank=True)
    google_place = models.ForeignKey(GooglePlace, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=50, choices=[('facebook', 'Facebook'),('instagram', 'Instagram')])
    permalink = models.URLField(max_length=1000)
    message = models.CharField(max_length=1000, null=True, blank=True)
    createdtime = models.CharField(max_length=1000, null=True, blank=True)
    ig_id = models.CharField(max_length=1000, blank=True)
    categories = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=1000, null=True, blank=True)
    
    def update_data(self):
        url = 'https://api.foursquare.com/v2/venues/search'
        lat = self.google_place.info['geometry']['location']['lat']
        lon = self.google_place.info['geometry']['location']['lng']
        name = self.google_place.info['name']
        split_names = name.split()
        mylist_distance = []
        mylist_category = []
        matched_venue = None
        for split_name in split_names:
            params = dict(
            client_id='2FMOM2DV2E2R5E4L5D1QFL4NS4MWC3VJU4C3YU5KEAWRVM4T',
            client_secret='THUSQ3S42S4KNIPROQEPP5VAWGBA2KXCYHSOUNJ4JZN1RGQY',
            v='20210403',
            ll=str(lat) + ',' + str(lon),
            query=split_name,
            locale='en'
            )
            resp = requests.get(url=url, params=params)
            form = resp.json()
            if form['response'].get('venues') and len(form['response']['venues']) > 0:
                category_name = form['response']['venues'][0]
                category_locations = form['response']['venues'][0]['location']['distance']
                mylist_distance.append(category_locations)
                mylist_category.append(category_name)
            near_distance = min(mylist_distance)
            for i in mylist_category:
                if near_distance is i['location']['distance']:
                    matched_venue = i
                    for restaurants in i['categories']:
                        restaurant_category = restaurants['name']  
                        self.categories = restaurant_category
        try:
            state = matched_venue['location']['state']
            city = matched_venue['location']['city']
            venue_id = matched_venue['id']
            foursquare_venue = FoursquareVenue.objects.filter(venue_id=venue_id).first()
            if not foursquare_venue:
                foursquare_venue = FoursquareVenue(venue_id=venue_id, data=matched_venue)
                foursquare_venue.save()
            self.foursquare = foursquare_venue
            self.state = state
            self.city = city
        except:
            self.city = ''
            self.state = ''
        self.save()



class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.URLField(max_length=1000, null=True, blank=True)
    image = models.ImageField(null=True, blank=1000, upload_to='postimage/')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)













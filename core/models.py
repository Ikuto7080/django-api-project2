from django.db import models
from django.contrib.auth.models import User
import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Connection(models.Model):
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followers = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    follow_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} : {}".format(self.follower.username, self.following.username)

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
    profile_picture = models.ImageField(null=True, blank=True, upload_to='profilepic/')
    inviter = models.OneToOneField("Account", null=True, blank=True, on_delete=models.SET_NULL)
    postkit_url = models.ImageField(null=True, blank=True, upload_to='invitepicture/')

    def __str__(self):
        return str(self.id)


class Device(models.Model):
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    fcm_token = models.CharField(max_length=1000, unique=True)


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
            ChineseRestaurant = ["Chinese Restaurant", "Anhui Restaurant","Beijing Restaurant","Cantonese Restaurant","Cha Chaan Teng","Chinese Aristocrat Restaurant","Chinese Breakfast Place","Dim Sum Restaurant","Dongbei Restaurant","Fujian Restaurant","Guizhou Restaurant","Hainan Restaurant","Hakka Restaurant","Henan Restaurant","Hong Kong Restaurant","Huaiyang Restaurant","Hubei Restaurant","Hunan Restaurant","Imperial Restaurant","Jiangsu Restaurant","Jiangxi Restaurant","Macanese Restaurant","Manchu Restaurant","Peking Duck Restaurant","Shaanxi Restaurant","Shandong Restaurant","Shanghai Restaurant","Shanxi Restaurant","Szechuan Restaurant","Taiwanese Restaurant","Tianjin Restaurant","Xinjiang Restaurant","Yunnan Restaurant","Zhejiang Restaurant"]
            IndonesianRestaurant = ["Indonesian Restaurant","Acehnese Restaurant","Balinese Restaurant","Betawinese Restaurant","Indonesian Meatball Place","Javanese Restaurant","Manadonese Restaurant","Padangnese Restaurant","Sundanese Restaurant"]
            JapaneseRestaurant = ["Japanese Restaurant","Donburi Restaurant","Japanese Curry Restaurant","Kaiseki Restaurant","Kushikatsu Restaurant","Monjayaki Restaurant","Nabe Restaurant","Okonomiyaki Restaurant","Ramen Restaurant","Shabu-Shabu Restaurant","Soba Restaurant","Sukiyaki Restaurant","Sushi Restaurant","Takoyaki Place","Tempura Restaurant","Tonkatsu Restaurant","Udon Restaurant","Unagi Restaurant","Wagashi Place","Yakitori Restaurant","Yoshoku Restaurant"]
            KoreanRestaurant = ["Korean Restaurant","Bossam/Jokbal Restaurant","Bunsik Restaurant","Gukbap Restaurant","Janguh Restaurant","Samgyetang Restaurant"]
            MalayRestaurant = ["Malay Restaurant","Mamak Restaurant"]
            DessertShop = ["Dessert Shop","Cupcake Shop","Frozen Yogurt Shop","Ice Cream Shop","Pastry Shop","Pie Shop"]
            FrenchRestaurant = ["French Restaurant","Alsatian Restaurant","Auvergne Restaurant","Basque Restaurant","Brasserie","Breton Restaurant","Burgundian Restaurant","Catalan Restaurant","Ch'ti Restaurant","Corsican Restaurant","Estaminet","Labour Canteen","Labour Canteen","Lyonese Bouchon","Norman Restaurant","Norman Restaurant","Provençal Restaurant","Savoyard Restaurant","Southwestern French Restaurant"]
            ItalianRestaurant = ["Italian Restaurant","Abruzzo Restaurant","Agriturismo","Aosta Restaurant","Basilicata Restaurant","Calabria Restaurant","Campanian Restaurant","Emilia Restaurant","Friuli Restaurant","Ligurian Restaurant","Lombard Restaurant","Malga,Marche Restaurant","Molise Restaurant","Piadineria","Piedmontese Restaurant","Puglia Restaurant","Romagna Restaurant","Roman Restaurant","Sardinian Restaurant","Sicilian Restaurant","South Tyrolean Restaurant","Trattoria/Osteria","Trentino Restaurant","Tuscan Restaurant","Umbrian Restaurant","Veneto Restaurant"]
            Bar =["Bar","Beach Bar","Beer Bar","Beer Garden","Champagne Bar","Cocktail Bar","Dive Bar","Gay Bar","Hookah Bar","Hotel Bar","Karaoke Bar","Pub","Sake Bar","Speakeasy","Sports Bar","Tiki Bar","Whisky Bar","Wine Bar"]
            for i in mylist_category:
                if near_distance is i['location']['distance']:
                    matched_venue = i
                    for restaurants in i['categories']:
                        if restaurants['name'] in ChineseRestaurant:
                            restaurant_category = "Chinese Restaurant"
                        elif restaurants['name'] in IndonesianRestaurant:
                            restaurant_category = "Indonesian Restaurant"
                        elif restaurants['name'] in JapaneseRestaurant:
                            restaurant_category = "Japanese Restaurant"
                        elif restaurants['name'] in KoreanRestaurant:
                            restaurant_category = "Korean Restaurant"
                        elif restaurants['name'] in MalayRestaurant:
                            restaurant_category = "Malay Restaurant"
                        elif restaurants['name'] in DessertShop:
                            restaurant_category = "Dessert Shop"
                        elif restaurants['name'] in FrenchRestaurant:
                            restaurant_category = "French Restaurant"
                        elif restaurants['name'] in ItalianRestaurant:
                            restaurant_category = "Italian Restaurant"
                        elif restaurants['name'] in Bar:
                            restaurant_category = "Bar"   
                        elif restaurants['name'] in ['BBQ Joint']:
                            restaurant_category = "BBQ Joint"  
                        elif restaurants['name'] in ['Bakery']:
                            restaurant_category = "Bakery"
                        elif restaurants['name'] in ['Café']:
                            restaurant_category = "Café"
                        elif restaurants['name'] in ['Tea Room']:
                            restaurant_category = "Tea Room"
                        else:
                            restaurant_category = "Others"  
                        # restaurant_category = restaurants['name']  
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
    image = models.ImageField(null=True, blank=True, upload_to='postimage/')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)













# -*- coding: utf-8 -*-
from instascrape import *
from celery import shared_task
from core.models import Account, Post, GooglePlace, IgLocation, PostImage, FoursquareVenue, Device
from instagram_basic_display.InstagramBasicDisplay import InstagramBasicDisplay
import requests
import facebook
from urllib import request
import uuid
from django.core.files import File
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging


@shared_task
def download_fb_post_2(post_url, user_id):#profile_picture
    try:
        full_picture = post_url.get('full_picture')
        if not full_picture:
            return []
        fb_permalink = post_url['permalink_url']
        place = post_url.get('place')
        if not place:
            return []
        location_name = post_url['place']['name']
        # profile_picture = profile_picture['url']
        try:
            message = post_url['message']
        except:
            message = ''
        created_time = post_url['created_time'].split('T')[0]
        latitude = post_url['place']['location']['latitude']
        longitude = post_url['place']['location']['longitude']
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?&key=AIzaSyBskgPF7N6t6bhxT1SoY2hP5OMe8knbdR0"
        params = {
        'input': location_name,
        'inputtype': 'textquery',
        'fields': 'place_id,name',
        'locationbias':'point:' + str(latitude) + ',' + str(longitude)
        }
        r = requests.get(url, params=params)
        form = r.json()
        place_id = form['candidates'][0]['place_id']
        detail_url = "https://maps.googleapis.com/maps/api/place/details/json?key=AIzaSyBskgPF7N6t6bhxT1SoY2hP5OMe8knbdR0"
        params = {
            'place_id': place_id,
            'fields': 'name,types,rating,formatted_phone_number,url,website,formatted_address,opening_hours,reviews,address_components,geometry,price_level'
        }
        r = requests.get(detail_url, params=params)
        form = r.json()
        google_info = form['result']
        is_restaurant = False
        for i in google_info['types']:
             if i in ['cafe', 'restaurant', 'bar']:
                 is_restaurant = True
                 break
        if not is_restaurant:
            return
        post = Post()
        post.permalink = fb_permalink
        post.message = message
        post.createdtime = created_time
        post.type = "facebook"
        post.user_id = user_id
        google_place = GooglePlace.objects.filter(place_id=place_id).first()
        if not google_place:
            google_place = GooglePlace(place_id=place_id, latitude=google_info['geometry']['location']['lat'], longitude=google_info['geometry']['location']['lng'])
        google_place.info = google_info
        google_place.save()
        post.google_place = google_place
        post.save()
        imagepost = PostImage()
        imagepost.url = full_picture
        result = request.urlretrieve(full_picture)
        f = open(result[0], 'rb')
        fb_file = File(f)
        imagepost.post = post
        imagepost.image.save(str(uuid.uuid4()), fb_file)
        imagepost.save()
    # foursquare for categories
        url = 'https://api.foursquare.com/v2/venues/search'
        lat = google_info['geometry']['location']['lat']
        lon = google_info['geometry']['location']['lng']
        name = google_info['name']
        split_names = name.split()
        mylist_distance = []
        mylist_category = []
        matched_venue = None
        for split_name in split_names:
            params = dict(
            client_id='2FMOM2DV2E2R5E4L5D1QFL4NS4MWC3VJU4C3YU5KEAWRVM4T',
            client_secret='THUSQ3S42S4KNIPROQEPP5VAWGBA2KXCYHSOUNJ4JZN1RGQY',
            v='20210516',
            ll=str(lat) + ',' + str(lon),
            query=split_name,
            locale='en'
            )
            resp = requests.get(url=url, params=params)
            form = resp.json()
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
                post.categories = restaurant_category
            # for i in mylist_category:
            #     if near_distance is i['location']['distance']:
            #         matched_venue = i
            #         for restaurants in i['categories']:
            #             restaurant_category = restaurants['name']  
            #             post.categories = restaurant_category
            #     elif near_distance >= 5000:
            #         restaurant_category = "Uncategories"
            #         post.categories = restaurant_category

        try:
            state = matched_venue['location']['state']
            city = matched_venue['location']['city']
            venue_id = matched_venue['id']
            foursquare_venue = FoursquareVenue.objects.filter(venue_id=venue_id).first()
            if not foursquare_venue:
                foursquare_venue = FoursquareVenue(venue_id=venue_id, data=matched_venue)
                foursquare_venue.save()
            post.foursquare = foursquare_venue
            post.state = state
            post.city = city
        except:
            post.city = ''
            post.state = ''
        post.save()
    except Exception as e:
        print(e)
        raise e

@shared_task
def get_fb_post(account_id):
    account = Account.objects.filter(id=account_id).first()
    user = account.user
    token = account.fb_token
    graph = facebook.GraphAPI(token)
    profile = graph.get_object('me', fields='first_name, last_name, picture, posts{permalink_url, place, full_picture, message,created_time}')# add parameter picture
    profile_picture = profile['picture']['data']['url']
    account.profile_picture = profile_picture
    account.save()
    post_urls = profile["posts"]["data"]
    for post_url in post_urls:
        download_fb_post_2.delay(post_url, user.id)
    page = profile['posts']
    page = page.get('paging')
    if not page:
        return []
    while True:
        if not page:
            break
        next_url = page.get('next')
        if not next_url:
            break
        r = requests.get(next_url)
        page = r.json()
        post_urls = page["data"]
        page = page.get('paging')
        for post_url in post_urls:
            download_fb_post_2.delay(post_url, user.id)
            print('paging correct')



@shared_task(rate_limit="1/s")
def download_ig_post_2(ig_profile, user_id):
    try:
        media_url = ig_profile['media_url']
        ig_permalink = ig_profile['permalink']
        try:
            message = ig_profile['caption']
        except:
            message = ''
        res = requests.get(ig_permalink, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'})
        bs = BeautifulSoup(res.text, 'html.parser')
        scripts = bs.find_all('script', {'type': 'text/javascript'})
        scripts_contents = scripts[3].contents[0]
        json_string = scripts_contents.split("window._sharedData = ")[1]
        json_string = json_string.split("location")[1]
        json_string = json_string.split(":")[2]
        json_string = json_string.split(",")[0]
        json_string = json_string.split('"')[1]

        post = Post()
        post.place_id = json_string
        url = 'https://www.instagram.com/explore/locations/' + str(json_string) + '/'
        place = Location(url)
        place.scrape()

        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?&key=AIzaSyBskgPF7N6t6bhxT1SoY2hP5OMe8knbdR0"
        params = {
            'input': place.name,
            'inputtype': 'textquery',
            'fields': 'place_id',
            'locationbias':'point:' + str(place.latitude) + ',' + str(place.longitude)
        }
        r = requests.get(url, params=params)
        form = r.json()
        place_id = form['candidates'][0]['place_id']
        detail_url = "https://maps.googleapis.com/maps/api/place/details/json?key=AIzaSyBskgPF7N6t6bhxT1SoY2hP5OMe8knbdR0"
        params = {
            'place_id': place_id,
            'fields':'name,types,rating,formatted_phone_number,international_phone_number,formatted_address,website,url,opening_hours,address_components,geometry'
        }
        r = requests.get(detail_url, params=params)
        form = r.json()
        google_info = form['result']
        is_restaurant = False
        for i in google_info['types']:
            if i in ['cafe', 'restaurant', 'bar']:
                is_restaurant = True
                break
        if not is_restaurant:
            return
        post.ig_permalink = ig_permalink
        post.message = message
        post.type = "instagram"
        post.user_id = user_id

        google_place = GooglePlace.objects.filter(place_id=place_id).first()
        if not google_place:
            google_place = GooglePlace(place_id=place_id, latitude=place.latitude, longitude=place.longitude)
        google_place.info = google_info
        google_place.save()
        post.google_place = google_place
        post.save()
        imagepost = PostImage()
        imagepost.url = media_url
        result = request.urlretrieve(media_url)
        f = open(result[0], 'rb')
        ig_file = File(f)
        imagepost.post = post
        imagepost.image.save(str(uuid.uuid4()), ig_file)
        imagepost.save()
    # foursquare for categories
        url = 'https://api.foursquare.com/v2/venues/search'
        lat = google_info['geometry']['location']['lat']
        lon = google_info['geometry']['location']['lng']
        name = google_info['name'] 
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
                        post.categories = restaurant_category
                elif near_distance >= 5000:
                    restaurant_category = "Uncategories"
                    post.categories = restaurant_category
        try:
            state = matched_venue['location']['state']
            city = matched_venue['location']['city']
            venue_id = matched_venue['id']
            foursquare_venue = FoursquareVenue.objects.filter(venue_id=venue_id).first()
            if not foursquare_venue:
                foursquare_venue = FoursquareVenue(venue_id=venue_id, data=matched_venue)
                foursquare_venue.save()
            post.foursquare = foursquare_venue
            post.state = state
            post.city = city
        except:
            post.city = ''
            post.state = ''
        post.save()
    except Exception as e:
        print(e)


@shared_task
def get_ig_post(account_id):
    account = Account.objects.filter(id=account_id).first()
    user = account.user
    instagram_basic_display = InstagramBasicDisplay(app_id='909807339845904', app_secret='f095f16729ea435ff0c36d6fda438d83', redirect_url='https://localhost:8080/insta/')
    instagram_basic_display.set_access_token(account.ig_token)
    ig_profile = instagram_basic_display.get_user_media()
    ig_profile_picture = instagram_basic_display.get_user_profile()
    username = ig_profile_picture['username']
    user_profile = Profile(username)
    user_profile.scrape()
    profile_picture = user_profile.profile_pic_url
    if not profile_picture:
        return profile_picture
    if profile_picture is not None:
        return []
    account.profile_picture = profile_picture
    account.save()
    ig_profiles = ig_profile['data']
    for ig_profile in ig_profiles:
        download_ig_post_2.delay(ig_profile, user.id)

@shared_task
def send_notification(account_id, follow_account_id):
    firebase_admin_sdk = {
        "type": "service_account",
        "project_id": "quouze-57e1a",
        "private_key_id": "832cdc14065f5ccc5d231c1cf9e9c60388794850",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDongMq4YrnTtYp\nSfcFPW8c9xuuPbR730EgNHA2ux2kzuYWw6EqPHkrZ4JYZzj6J8Ub+uEF9w6tP9eF\nfJyDC7mTflxvb+mfpH4ogsjQGoQjQKNfA6KXHYZBru9J2qvRh49QHMnSKdAUwIRA\nepsSSDr7vAxQ2/0GC6G3wd3OnqfaMI0XLNDiSTf8MNuFmXAOMaTZoKJuyv2UYdMZ\nXd2Mk8ZiqTZR7Um1YlczNC2Gqw/pOUQMGNN1xg/QL/gE80yYLmC8fPLdZKKhnwCR\nL9sgDJrI9CupBBPEFgaiYos0XhvMqIj/F2pYuxRiofswg5BtKYi7rCFC3ZLR0mJn\n3ExEr9BZAgMBAAECggEAF8sd2NOEIT/LoSKLLVKI3IYcIzj1jpwZ7cDfX4HJOPPe\nziJJiGfyHvHx/7fjOJc7zq5dOP551lfK5EEIQ1E+NKt+qflhBK7PJral8r9bl72D\nWHMnPNzMwEgz+rJu07pReujO7fvP6Gd+v5eq5/ZSbjBgdB7kZStoacLfPMS2t5cA\n02KLGx47vv0Z6Xia6ZJ3E5gHHmRsSW3PfK3829HUhCWx7l8Vvuv8Oiv9Nsijy/Li\ny9fR+V19fXVciTtiWeWlYS5e3CVkt10d1oA1obEtnQwBt/33LXTrMALGgudEQqVd\nx3aOd/o8eRmR8OJN0KCMIxVWXTBybgqr9gB1AKks7wKBgQD090kDw1vqW4DgeX70\nzsvHehPsEHmLMkoPi09Q5+IiHIjJX6mu/TT+uf/dS1QzlLnoN30eEZEU6rJs6OE0\n0DBlHLwEd8f29jzvGeRugCRb9MV/em84QNgVmRbT2ei8al3Wo/4UR7sL7rSEEmUC\nXAKdNAL0P7qGG3NmK2/wWquJuwKBgQDzGFVbStTUSvCZqZ0EEnRBnfwVHk/RIsCt\nVEwDXHimn5hueKtvkMuiIlDr3FSkg3GjtmpWUBUslRHtTyHmZGBPHJ9EHIv32MIM\ncI1tz+/o5R1TGyym/JV3GfxbzrbcSNCb+835CWSHfq0YnucFQey1vFfzJ6cfLV01\nm78E25fy+wKBgQCkfZRq0XjcArukgBDvBBm0BdZw0pM7E/bFP09wTXT8YNq9Fd6U\nIXS/g1g7WcTdqgW31+LNGRCp0fsjxLDMzOtiSgw6l9APlkNObr2EMcm4ccFYm3cp\nd+lhf13jvdRZCLegVJhdN9ly5sQSV2O6VNxwgSdmqZBvUumHdq2A4PGE1wKBgQCA\nqAc8ysz7EjJmURNNvWqT88YfcyxxFgB9e5jDSqR8IwkspmatJCfxxlGnkrOlYf+5\n0mhTCA08zCRxwSjC46rpE8/i32zgnnKM3OCtFpj1XJT5j+9A7Xs5TqJ2AGBdE5h8\nhXcMb4EqCMwZtLe1258oy+aMRRc48+xZ2/Tr4EB6EwKBgQCqwylcJAvCy4r45Am2\nVBip7xVXo7VFsnp4UbSzSlnPVZDwolZ4/BjlnXtir5YtiantfzCrBG2wbsRBIHxq\nS43GxNtYmkCtSvQLT8ZQ9E7HwwXNMjotxAod3t1/3l/DFaAXcZIEnprSTS5qssXf\nmtUMXGhkSqQqSLTCLJKKvdMFWw==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-4vq80@quouze-57e1a.iam.gserviceaccount.com",
        "client_id": "118246523264564474499",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-4vq80%40quouze-57e1a.iam.gserviceaccount.com"
        }

    cred = credentials.Certificate(firebase_admin_sdk)
    firebase_admin.initialize_app(cred)

    devices = Device.objects.filter(account=follow_account_id).all()
    account = Account.objects.get(id=account_id)
    for device in devices:
        try:
            # See documentation on defining a message payload.
            message = messaging.Message(
                notification=messaging.Notification(
                    title='通知',
                    body=f'{account.user.first_name}がquouzeにログインしました',
                ),
                token=device.fcm_token
            )

            # Send a message to the device corresponding to the provided
            # registration token.
            response = messaging.send(message)
            # Response is a message ID string.
            print('Successfully sent message:', response)
        except:
            pass

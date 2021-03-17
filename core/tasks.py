# -*- coding: utf-8 -*-
from celery import shared_task
from core.models import Account, FbPost, IgPost
from instagram_basic_display.InstagramBasicDisplay import InstagramBasicDisplay
import requests
import facebook
from urllib import request
import uuid
from django.core.files import File
from bs4 import BeautifulSoup
from instascrape import *

@shared_task
def hello(name):
    print(name)

@shared_task
def download_fb_post(post_url, user_id):
    post = FbPost()
    post.user_id = user_id
    print(post_url)
    try:
        full_picture = post_url['full_picture']
        permalink_url = post_url['permalink_url']
        location_name = post_url['place']['name']
        latitude = post_url['place']['location']['latitude']
        longitude = post_url['place']['location']['longitude']
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?&key=AIzaSyCh-n6Zenl66RuVS6c9N4xEKKG9-boLa7I"
        params = {
        'input': location_name,
        'inputtype': 'textquery',
        'fields': 'place_id,name',
        'locationbias':'point:' + str(latitude) + ',' + str(longitude)
        }
        r = requests.get(url, params=params)
        form = r.json()
        place_id = form['candidates'][0]['place_id']
        detail_url = "https://maps.googleapis.com/maps/api/place/details/json?key=AIzaSyCh-n6Zenl66RuVS6c9N4xEKKG9-boLa7I"
        params = {
            'place_id': place_id,
            'fields': 'name,types,rating,formatted_phone_number,url,website,formatted_address,opening_hours'
        }
        r = requests.get(detail_url, params=params)
        form = r.json()
        google_info=form['result']
        post.google_info = google_info
        post.post_url = full_picture
        post.permalink_url = permalink_url
        post.latitude = latitude
        post.longitude = longitude
        post.location_name=location_name
        for i in google_info['types']:
            print(i)
            if i in ['cafe', 'restaurant', 'bar']:
                post.save()
                print(post.id)
    except Exception as e:
        print(e)

@shared_task
def get_fb_post(account_id):
    account = Account.objects.filter(id=account_id).first()
    user = account.user
    token = account.fb_token
    graph = facebook.GraphAPI(token)
    profile = graph.get_object('me', fields='first_name, last_name,posts{permalink_url, place, full_picture, message}')
    post_urls = profile["posts"]["data"]
    for post_url in post_urls:
        download_fb_post.delay(post_url, user.id)

@shared_task
def download_ig_post(ig_profile, user_id):
    post = IgPost()
    post.user_id = user_id
    print(ig_profile)
    try:
        media_url = ig_profile['media_url']
        permalink = ig_profile['permalink']
        res = requests.get(permalink, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'})
        bs = BeautifulSoup(res.text, 'html.parser')
        scripts = bs.find_all('script', {'type': 'text/javascript'})
        scripts_contents = scripts[3].contents[0]
        json_string = scripts_contents.split("window._sharedData = ")[1]
        json_string = json_string.split("location")[1]
        json_string = json_string.split(":")[2]
        json_string = json_string.split(",")[0]
        json_string = json_string.split('"')[1]
        result = request.urlretrieve(media_url)
        f = open(result[0], 'rb')
        ig_file = File(f)
        post.place_id = json_string
        url = 'https://www.instagram.com/explore/locations/' + str(json_string) + '/'
        place = Location(url)
        place.scrape()
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?&key=AIzaSyCh-n6Zenl66RuVS6c9N4xEKKG9-boLa7I"
        params = {
            'input': place.name,
            'inputtype': 'textquery',
            'fields': 'place_id',
            'locationbias':'point:' + str(place.latitude) + ',' + str(place.longitude)
        }
        r = requests.get(url, params=params)
        form = r.json()
        place_id = form['candidates'][0]['place_id']
        detail_url = "https://maps.googleapis.com/maps/api/place/details/json?key=AIzaSyCh-n6Zenl66RuVS6c9N4xEKKG9-boLa7I"
        params = {
            'place_id': place_id,
            'fields': 'name,types,rating,formatted_phone_number,url,website,formatted_address,opening_hours'
        }
        r = requests.get(detail_url, params=params)
        form = r.json()
        google_info=form['result']
        post.google_info = google_info
        post.media_url = media_url
        post.permalink = permalink
        post.latitude = place.latitude
        post.longitude = place.longitude
        post.location_name = place.name
        post.location_id = str(json_string)
        print(google_info)
        for i in google_info['types']:
            if i in ['cafe', 'restaurant', 'bar']:
                post.image.save(str(uuid.uuid4()), ig_file)
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
    ig_profiles = ig_profile['data']
    for ig_profile in ig_profiles:
        download_ig_post.delay(ig_profile, user.id)



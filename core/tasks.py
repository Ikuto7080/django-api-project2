# -*- coding: utf-8 -*-
from instascrape import *
from celery import shared_task
from core.models import Account, ALLPost, Post, GooglePlace, IgLocation, PostImage
from instagram_basic_display.InstagramBasicDisplay import InstagramBasicDisplay
import requests
import facebook
from urllib import request
import uuid
from django.core.files import File
from bs4 import BeautifulSoup


@shared_task
def download_fb_post_2(post_url, user_id):
    try:
        full_picture = post_url['full_picture']
        fb_permalink = post_url['permalink_url']
        location_name = post_url['place']['name']
        try:
            message = post_url['message']
        except:
            message = ''
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
            'fields': 'name,types,rating,formatted_phone_number,url,website,formatted_address,opening_hours,reviews'
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
        post.type = "facebook"
        post.user_id = user_id
    # foursquare for categories
        url = 'https://api.foursquare.com/v2/venues/search'
        query_name = form['result']['name']
        params = dict(
        client_id='2FMOM2DV2E2R5E4L5D1QFL4NS4MWC3VJU4C3YU5KEAWRVM4T',
        client_secret='THUSQ3S42S4KNIPROQEPP5VAWGBA2KXCYHSOUNJ4JZN1RGQY',
        v='20210403',
        ll=str(latitude) + ',' + str(longitude),
        query=query_name,
        limit=1
        )
        resp = requests.get(url=url, params=params)
        form = resp.json()
        category_form = form['response']['venues'][0]['categories'][0]['name']
        post.categories = category_form
        print(category_form)

        google_place = GooglePlace.objects.filter(place_id=place_id).first()
        if not google_place:
            google_place = GooglePlace(place_id=place_id, latitude=latitude, longitude=longitude)
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
        download_fb_post_2.delay(post_url, user.id)
    page = profile['posts']
    while True:
        next_url = page['paging'].get('next')
        if not next_url:
            break
        r = requests.get(next_url)
        page = r.json()
        post_urls = page["data"]
        for post_url in post_urls:
            download_fb_post_2.delay(post_url, user.id)



@shared_task
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
        result = request.urlretrieve(media_url)
        f = open(result[0], 'rb')
        ig_file = File(f)
        post = Post()
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
            'fields': 'name,types,rating,formatted_phone_number,url,website,formatted_address,opening_hours,reviews,price_level'
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
        post.type = "instagram"
        post.user_id = user_id

        google_place = GooglePlace.objects.filter(place_id=place_id).first()
        if not google_place:
            google_place = GooglePlace(place_id=place_id, latitude=place.latitude, longitude=place.longitude)
        google_place.info = google_info
        google_place.save()

    # foursquare for categories
        url = 'https://api.foursquare.com/v2/venues/search'
        params = dict(
        client_id='2FMOM2DV2E2R5E4L5D1QFL4NS4MWC3VJU4C3YU5KEAWRVM4T',
        client_secret='THUSQ3S42S4KNIPROQEPP5VAWGBA2KXCYHSOUNJ4JZN1RGQY',
        v='20210403',
        ll=str(place.latitude) + ',' + str(place.longitude),
        query=place.name,
        limit=1
        )
        resp = requests.get(url=url, params=params)
        form = resp.json()
        category_form = form['response']['venues'][0]['categories'][0]['name']
        post.categories = category_form
        print(category_form)

        post.google_place = google_place
        post.ig_id = json_string
        post.permalink = ig_permalink
        post.message = message
        post.save()
        imagepost = PostImage()
        imagepost.url = media_url
        result = request.urlretrieve(media_url)
        f = open(result[0], 'rb')
        ig_file = File(f)
        imagepost.post = post
        imagepost.image.save(str(uuid.uuid4()), ig_file)
        imagepost.save()
        ig_location = IgLocation(ig_id=json_string)
        ig_location.save()
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
        download_ig_post_2.delay(ig_profile, user.id)




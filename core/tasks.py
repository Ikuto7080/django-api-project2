# -*- coding: utf-8 -*-
from celery import shared_task
from core.models import Account, FbPost, IgPost
from instagram_basic_display.InstagramBasicDisplay import InstagramBasicDisplay
import requests
import facebook
import requests
from bs4 import BeautifulSoup
from instascrape import *

@shared_task
def hello(name):
    print(name)


@shared_task
def get_fb_post(account_id):
    account = Account.objects.filter(id=account_id).first()
    user = account.user
    post = FbPost()
    post.user = user
    token = account.fb_token
    graph = facebook.GraphAPI(token)
    #fields = ['first_name', 'location{location}','email','link']
    profile = graph.get_object('me', fields='first_name, last_name, location,link,email, posts{full_picture,message}')
    post_urls = profile["posts"]["data"]
    post_url = post_urls[0]['full_picture']
    post.post_url = post_url
    post.save()
    print(post.post_url)

@shared_task
def get_ig_post(account_id):
    account = Account.objects.filter(id=account_id).first()
    user = account.user
    post = IgPost()
    post.user = user
    instagram_basic_display = InstagramBasicDisplay(app_id='909807339845904', app_secret='f095f16729ea435ff0c36d6fda438d83', redirect_url='https://localhost:8080/insta/')
    instagram_basic_display.set_access_token(account.ig_token)
    ig_profile = instagram_basic_display.get_user_media()
    media_url = ig_profile['data'][0]['media_url']
    permalink = ig_profile['data'][0]['permalink']
    res = requests.get(permalink, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'})
    bs = BeautifulSoup(res.text, 'html.parser')
    scripts = bs.find_all('script', {'type': 'text/javascript'})
    scripts_contents = scripts[3].contents[0]
    json_string = scripts_contents.split("window._sharedData = ")[1]
    json_string = json_string.split("location")[1]
    json_string = json_string.split(":")[2]
    json_string = json_string.split(",")[0]
    json_string = json_string.split('"')[1]
    print(media_url)
    post.media_url = media_url
    post.image = media_url
    post.permalink = permalink
    post.place_id = json_string
    url = 'https://www.instagram.com/explore/locations/' + str(json_string) + '/'
    place = Location(url)
    place.scrape()
    post.latitude = place.latitude
    post.longitude = place.longitude
    post.location_name = place.name
    post.save()
    


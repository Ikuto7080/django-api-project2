from core.models import Account, ALLPost, Post, GooglePlace, IgLocation, PostImage, FoursquareVenue
import requests
import facebook
from urllib import request
import uuid
from django.core.files import File
from bs4 import BeautifulSoup
from math import radians, cos, sin, asin, sqrt
import numpy as np


def download_fb_post_2(post_url, user_id):#profile_picture
    try:
        nom = 0
        place = post_url.get('place')
        if place:
            print(post_url['id'], place)
        if not place:
            print(post_url['id'], 'no place')
            return []
    except Exception as e:
        print(e)
        raise e


account_id=9
account = Account.objects.filter(id=account_id).first()
user = account.user
token = account.fb_token
graph = facebook.GraphAPI(token)
profile = graph.get_object('me', fields='id, first_name, last_name, picture, posts{permalink_url, place, full_picture, message}')# add parameter picture
profile_picture = profile['picture']['data']['url']
account.profile_picture = profile_picture
post_urls = profile["posts"]["data"]
for post_url in post_urls:
    download_fb_post_2(post_url, user.id)
page = profile['posts']
page = page.get('paging')
# if not page:
#     return []
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
        download_fb_post_2(post_url, user.id)




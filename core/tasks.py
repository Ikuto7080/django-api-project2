# -*- coding: utf-8 -*-
from celery import shared_task
from core.models import Account, FbPost, IgPost
from instagram_basic_display.InstagramBasicDisplay import InstagramBasicDisplay
import requests
import facebook

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
    instagram_basic_display = InstagramBasicDisplay(app_id='909807339845904', app_secret='f095f16729ea435ff0c36d6fda438d83', redirect_url='https://obscure-reef-20222.herokuapp.com/insta/')
    instagram_basic_display.set_access_token(account.ig_token)
    ig_profile = instagram_basic_display.get_user_media()
    media_url = ig_profile['data'][0]['media_url']
    print(media_url)
    post.media_url = media_url
    post.save()
    # for media_url in media_urls:
    #     post.media_url = media_url['media_url']
    #     post.save()
    #     print(post.media_url)

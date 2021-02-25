# -*- coding: utf-8 -*-
from core.models import Account, Post
import facebook


account = Account.objects.filter(id=14).first()
user = account.user
post = Post()
post.user = user
token = account.fb_token
graph = facebook.GraphAPI(token)
#fields = ['first_name', 'location{location}','email','link']
profile = graph.get_object('me', fields='first_name, last_name, location,link,email, posts{full_picture,message}')
post_urls = profile["posts"]["data"]
post_url = post_urls[1]
post.post_url = post_url.values()
post.save()
# for post_url in post_urls:
#     print(post_url.values(1))

print(post.post_url)
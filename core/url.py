# -*- coding: utf-8 -*-
import requests
import facebook
parameter = "AQBb2Sjxzq_MowoN_iJc3XrCVV4K3NGW6ywGfLoG-rcqNciDAgCTCkAL9iXy-yJHTqjTWAl51EZsOlngI_rbt1MF1ar-JUOOKn6pPKXlznm1j5SyRVA3LLYBif0SG1uN5pIe6dAhUarNJP7wdkGI-CFLdcb4SHs32uC2n_4Kusgoo6lhyFdqRqyZTClEJDnYltsLYNf3ZijTUCN0zzO7QcJxXNs-wSiE8B5bFseXc86S1L6oRMNQZ-0Gnl2YdMetCgTpcvVultQ4Xj_g0TwcY9mpTpcYjiPthN6wtLvJXwlmHVHdK7wxK0H6FoKXyg6HX4HU3LqxAGgFR8PZr_RHmApJ"
url = "https://graph.facebook.com/v9.0/oauth/access_token"
params = {
    'client_id': '420945845838455',
    'redirect_uri': 'https://obscure-reef-20222.herokuapp.com/fb_user_info/',
    'client_secret': '86f24082416e7e017e2c4f8f4e39458f',
    'code': parameter
}
r = requests.get(url, params=params)
form = r.json()
fb_token = form['access_token']
token = fb_token
graph = facebook.GraphAPI(token)
#fields = ['first_name', 'location{location}','email','link']
profile = graph.get_object('me', fields='first_name, last_name, location,link,email, posts{full_picture,message}')
print(profile)








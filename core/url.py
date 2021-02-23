# -*- coding: utf-8 -*-
import requests
parameter = "AQDOgbQUaFtwEGNiVKMYDkvBLUicgwztWllRIxXCFZJniqmURG1E7qjXpAQQGyB-ipRrzPOt6DLHHf-VKvtryz7r5Rw43iHTky8f5IudKuwRNjQmKmDtcBqKh299GRmRbD12xyH0hWROQmPKkqhWDbAIbIz7uyTgKIPu1nYkA9OkLOcRO2Xsc7JC_xUs1UhkdeEZWWcngi6u2tYGcdkWEHkZqqsqgb8JH1pDWu_RU-ir0FX5NPZxx7mBbzrcAZKiP7YAOxen728kXlPY6cyJe8zEIAZzVHvCzahuvdG0BVLRaOAiNcJi5ONSmf56kfLUNQifb9_M3GD1L5Yaozs7815l"

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
print(fb_token)
# token = fb_token
# graph = facebook.GraphAPI(token)
# #fields = ['first_name', 'location{location}','email','link']
# profile = graph.get_object('me', fields='first_name, last_name, location,link,email')
# print(profile)
# #Accountが存在するか確認する
# fb_id = profile['id'] 







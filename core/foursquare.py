import json, requests
url = 'https://api.foursquare.com/v2/venues/search'

params = dict(
client_id='2FMOM2DV2E2R5E4L5D1QFL4NS4MWC3VJU4C3YU5KEAWRVM4T',
client_secret='THUSQ3S42S4KNIPROQEPP5VAWGBA2KXCYHSOUNJ4JZN1RGQY',
v='20210403',
ll='40.7243,-74.0018',
query='coffee',
limit=1
)
resp = requests.get(url=url, params=params)
form = resp.json()
form = form['response']['venues'][0]['categories'][0]['name']
print(form)

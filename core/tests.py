import requests
url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?&key=AIzaSyCh-n6Zenl66RuVS6c9N4xEKKG9-boLa7I"

params = {
    'input': '神戸三宮',
    'inputtype': 'textquery',
    'fields': 'name,types',
    'locationbias':'point:34.6956056791,135.197755581'
}

r = requests.get(url, params=params)
form = r.json()
# print(form)
name = form['candidates'][0]['name']
types = form['candidates'][0]['types']
for i in types:
    print(i)
# print(name)
# print(types)

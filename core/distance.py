from math import radians, cos, sin, asin, sqrt
import requests
import numpy as np


def haversine(lon1, lat1, lon2, lat2, mylist_km, num):

    #foursquare
    foursquare_url = 'https://api.foursquare.com/v2/venues/search?client_id=S0V1PZWTH3WRIZT1IA1FQDEYXPRSTD5BIN0RMQEUYFBYTAKA&client_secret=SCVKAW3X2DGYBCCH103MVQLX5NSCPQE3MU4BFOHWSHR3QSQD'
    lat = google_info['geometry']['location']['lat']
    lon = google_info['geometry']['location']['lng']
    location_name = 'くら寿司 八王子インター店'
    params = {
        'v': '202100506',
        'query': location_name,
        'll': str(lat) +  ',' + str(lon),
        # 'radius': 1000
    }
    r = requests.get(foursquare_url, params=params)
    form = r.json()
    category_name = form['response']['venues']

    #longitude2,latitude2  make for

    mylist_lat = []
    mylist_lon = []

    for category in category_name:
        lats = category['location']['lat']
        lons = category['location']['lng']
        mylist_lat.append(lats)
        mylist_lon.append(lons)

    mylist_km = []
    for i, (lati, loni) in enumerate(zip(mylist_lat, mylist_lon)):
        lat = google_info['geometry']['location']['lat']
        lon = google_info['geometry']['location']['lng']
        lon1, lat1, lon2, lat2 = map(radians, [lon, lat, loni, lati])
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        km = 6371* c
        mylist_km.append(km)

        
    num = 0
    idx = np.abs(np.asarray(mylist_km) - num).argmin()
    smallest = mylist_km[idx]

    for category in category_name:
        distance = smallest
        list = mylist_km
        if distance is list:
            for i in category['categories']:
            restaurant_category = i['name']
            return restaurant_category
            post.categories = restaurant_category
            post.save()
            print(restaurant_category)
    



    



    # for category in category_name:
    #     smallest = distance
    #     if min(mylist_km):
    #         for i in category['categories']:
    #         restaurant_category = i['name']
    #         print(restaurant_category)
    


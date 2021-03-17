from instascrape import *


url = 'https://www.instagram.com/p/CMS7cOCB8zn/'
place = Post(url)
place.scrape()
latitude = place.latitude
longitude = place.longitude
location_name = place.name
print(location_name)
print(latitude)
print(longitude)


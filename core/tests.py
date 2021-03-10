import requests
import datetime

url = "https://scontent-nrt1-1.cdninstagram.com/v/t51.29350-15/109130871_149225830105794_6871359187132379915_n.jpg?_nc_cat=107&ccb=1-3&_nc_sid=8ae9d6&_nc_ohc=QnKpVyNkJ7YAX-2HEmk&_nc_ht=scontent-nrt1-1.cdninstagram.com&oh=cca63e1391b65a1478c5e97d445336cb&oe=606F1FBB"
now = datetime.datetime.now()
# print(now)
time_now = "{0:%Y%m%d_%H%M-%S_%f}".format(now) + ".jpg"
print(time_now)
file_name = time_now


response = requests.get(url)
image = response.content

with open(file_name, "wb") as aaa:
    aaa.write(image)
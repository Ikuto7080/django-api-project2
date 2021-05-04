from core.tasks import download_fb_post_2

post_url = {
      "permalink_url": "https://www.facebook.com/3819299764790837/posts/3596024023785080",
      "place": {
        "name": "都城焼肉党",
        "location": {
          "city": "Miyakonojo-shi",
          "country": "Japan",
          "latitude": 31.7257178,
          "longitude": 131.0629464,
          "state": "Miyazaki",
          "street": "宮崎県都城市中町2-5",
          "zip": "885-0071"
        },
        "id": "479601072555722"
      },
      "full_picture": "https://external-itm1-1.xx.fbcdn.net/safe_image.php?d=AQEowHq7EcPfBfpO&url=https%3A%2F%2Fassets.st-note.com%2Fproduction%2Fuploads%2Fimages%2F41519319%2Frectangle_large_type_2_d605640d7dee8f7a943c837941152884.jpg%3Ffit%3Dbounds%26quality%3D85%26width%3D1280&ccb=3-5&_nc_hash=AQFG-jbR9AUDHaYl",
      "message": "故郷都城のコロナ渦。直撃する私の経営する焼肉店、都城焼肉党のピンチをどう乗り越える？",
      "created_time": "2021-01-26T09:56:21+0000",
      "id": "3819299764790837_3596024023785080"
    }

download_fb_post_2(post_url, 61)
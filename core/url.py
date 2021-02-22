import requests
parameter = "AQD9MlbccaNXbmLsLxtQen_H7q7sCCIOXtbIvo6yOsZbDGp2R2PeMN0GU3YBy_-KRJB4h5_EQtWIflB_2S16vkK1MrrQ91khvG07HEhcpRapq6a4aXdgbqOvUvuQI5OUp7d09KWjYCdqTKz0Si2icl4B5TYUhnMBX_B4pk44eS4lsO72-52LGZjM4bNfn_c3u0WTgeWMvAskXXF-qD5zkAtmQS1xHWfoGxXfEJjp4iKt3Idj5BNnzPq53JYZKIxPwLSlXlb9zbSC9nX5LZhE0fF02zWG9qlDmBJkaFzPFMK_A2pMRoqZfJtxSD0KhJhwjIn9qsCDe96AFaoEgXPC2okH"

url = "https://graph.facebook.com/v9.0/oauth/access_token"
params = {
    'client_id': '420945845838455',
    'redirect_uri': 'https://localhost:8080/',
    'client_secret': '86f24082416e7e017e2c4f8f4e39458f',
    'code': parameter
}
r = requests.get(url, params = params)
print(r.json())




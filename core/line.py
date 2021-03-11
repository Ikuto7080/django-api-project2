from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

line_bot_api = LineBotApi('6uwpQB6+n8WdqkWPQIPYEiuh168/EPrOSdhmwBf813v9MSq4F3JqZ7V4wCAan3BBH7/sKrfNLzHFmHIfN3z9cefAfAh+yos1feTZCUORRCTsTe0tBLNIHJzLPNMTzN4Oj6n1wwxf6CyVFxugHa9kAwdB04t89/1O/w1cDnyilFU=')

try:
    message = line_bot_api.push_message('Ue83e0d212bef825fcc6f21d43100c632', TextSendMessage(text='I like you.'))
    print(message)
except LineBotApiError as e:
    print(e)
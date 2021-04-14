from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

line_bot_api = LineBotApi('YuF0YC+YQxY5f9g1lTPKNwW0BzN/r7f9q6DZ7KpnpmVnch26f/mWLSzEUJRFZo95K8J4CTBwYUjwO8TIyZwY+xYbp3UFRPYfIfgkuA57PaCnOsC8piCgEyZhWu/IwVZMwNlCJtI6ZWvyOLzgnozCiAdB04t89/1O/w1cDnyilFU=')

try:
    message = line_bot_api.push_message('Ud5aad5ed99b0ccf7f446323bf5c48c15', TextSendMessage(text='test.'))
    print(message)
except LineBotApiError as e:
    print(e)



from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

line_bot_api = LineBotApi('OvDbZDGVmDjD0r38Y6RQCSna0V6fuGHckqKMbcxLoA3a1y0Yf4fadCCY84bYR41fK8J4CTBwYUjwO8TIyZwY+xYbp3UFRPYfIfgkuA57PaDXXMnib8/16ZMnvO7rDLjZxrnhtbj59il5tY8C2BWYbgdB04t89/1O/w1cDnyilFU=')

try:
    message = line_bot_api.push_message('Ud5aad5ed99b0ccf7f446323bf5c48c15', TextSendMessage(text='I like you.'))
    print(message)
except LineBotApiError as e:
    print(e)
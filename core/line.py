from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

line_bot_api = LineBotApi('GxPeBqxjprRN3dtP3cyN+0RxFRGXh3d9RFJ/zyliBGdPJqbQGuXGoov9Mwa+gl+qpH/KQfk40duLxhnTaSYfvmoH5Fl7HhNn4rrAa9VAVBUTRJpSz/00uneI/gj+G6lgiO7nQIcHGNVtD1KB3E35WwdB04t89/1O/w1cDnyilFU=')

try:
    message = line_bot_api.push_message('Ud5aad5ed99b0ccf7f446323bf5c48c15', TextSendMessage(text='I like you.'))
    print(message)
except LineBotApiError as e:
    print(e)
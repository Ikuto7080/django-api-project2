import json
import facebook
from rest_framework import views, response
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

# importしたときに内容が表示されない

def main():
    token = "EAAFZB2RecYncBAH6ysfvP6QBHCDwh3rPA17qt9ZAeG9wa6f1DK58n3LjG0ab7mV80lMRJnVQqmZCA6A42GAOLSfhQK7zP6c782eROceJvv9g0ozZB5lrLeySb70zh24lfBgW9KmSAGkdLFI4e1ivZAhxZCVwYI674g7dnpbhCIKiisVWIMYwaoinDcoAUo2tgZD"
    graph = facebook.GraphAPI(token)
    #fields = ['first_name', 'location{location}','email','link']
    profile = graph.get_object('me',fields='first_name, last_name, location,link,email')
    #return desired fields
    print(json.dumps(profile, indent=4))

if __name__ == '__main__':
    main()


class LineWebHookView(views.APIView):
    def post(self, request):
        try:
            line_bot_api = LineBotApi('a5CLrs/QnqvkpHzgqmPYdRbo8TRt8eYF3DVA/6BqFRQZaq78ud84wFw/7FfNbbeIpH/KQfk40duLxhnTaSYfvmoH5Fl7HhNn4rrAa9VAVBVLcPQkWD7DH4kNqC3gnsH1ho/b3AtT7S8dXNS1DzSYQQdB04t89/1O/w1cDnyilFU=')
            user_id = request.data['events'][0]['source']['userId']
            line_bot_api.push_message(user_id, TextSendMessage(text='http://localhost:8080/login/' + '?user_id=' + user_id))
        except LineBotApiError as e:
            print(e)
        return response.Response({'status': 'Ok'})






        

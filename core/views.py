import json
import facebook
import os
from rest_framework import views, response
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from core.models import ApiSetting

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
            line_token = ApiSetting.objects.get(name="line_channel_token")
            line_bot_api = LineBotApi(line_token.value)
            user_id = request.data['events'][0]['source']['userId']
            text = request.data['events'][0]['message']['text']
            domain_url = os.environ.get('DOMAIN_URL', 'https://app.quouze.com')
            try:
                request_id = text.split('=')[-1]
                #send push messages
                line_bot_api.push_message(user_id, TextSendMessage(text=domain_url + '/login/?user_id=' + user_id + '&inviter_id=' + str(request_id)))
            except:
                line_bot_api.push_message(user_id, TextSendMessage(text='Go to this url to sign up!'))
                line_bot_api.push_message(user_id, TextSendMessage(text=domain_url + '/login/?user_id=' + user_id))
        except Exception as e:
            print(e)
        return response.Response({'status': 'Ok'})
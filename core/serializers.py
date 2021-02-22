from django.contrib.auth.models import User
from rest_framework import serializers
from core.models import Account
import uuid
import facebook
import requests
from instagram_basic_display.InstagramBasicDisplay import InstagramBasicDisplay
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'first_name', 'last_name', 'email', 'is_staff']



class AccountSerializer(serializers.ModelSerializer):
    fb_code = serializers.CharField(required=False, write_only=True)
    ig_code = serializers.CharField(required=False, write_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Account
        fields = ['id', 'user', 'fb_token' , 'ig_token', 'fb_code', 'ig_code', 'fb_id', 'ig_id']
        read_only_fields = ['user', 'fb_token', 'ig_token', 'fb_id', 'ig_id']

    



    def create(self, validated_data):
          fb_code = validated_data.get("fb_code")
          ig_code = validated_data.get("ig_code")
          if fb_code:
                url = "https://graph.facebook.com/v9.0/oauth/access_token"
                params = {
                'client_id': '420945845838455',
                'redirect_uri': 'https://localhost:8080/fb_user_info/',
                'client_secret': '86f24082416e7e017e2c4f8f4e39458f',
                'code': fb_code
                }
                r = requests.get(url, params=params)
                form = r.json()
                fb_token = form['access_token']
                token = fb_token
                graph = facebook.GraphAPI(token)
                #fields = ['first_name', 'location{location}','email','link']
                profile = graph.get_object('me', fields='first_name, last_name, location,link,email')
                #Accountが存在するか確認する
                fb_id = profile['id'] 
                account = Account.objects.filter(fb_id=fb_id).first()
                if account:
                      return account  
                #userのfb_id
                user = User(username=str(uuid.uuid4()))
                user.first_name = profile['first_name']
                user.last_name = profile['last_name']
                user.email = profile.get('email', '')
                user.save()
                account = Account()
                account.user = user
                account.fb_id = profile['id']
                account.fb_token = fb_token
                account.save()
                return account

          elif ig_code:
                instagram_basic_display = InstagramBasicDisplay(app_id ='909807339845904', app_secret='f095f16729ea435ff0c36d6fda438d83', redirect_url='https://localhost:8080/insta/')
                auth_token = instagram_basic_display.get_o_auth_token(ig_code)
                instagram_basic_display.set_access_token(auth_token['access_token'])
                ig_profile = instagram_basic_display.get_user_profile()
                ig_id = ig_profile['id'] 
                account = Account.objects.filter(ig_id=ig_id).first()
                if account:
                      return account  
                user = User(username=str(uuid.uuid4()))
                user.first_name = ig_profile['username']
                user.save()
                account = Account()
                account.user = user
                account.ig_id = ig_profile['id']
                account.ig_token = auth_token
                account.save()
                return account
          else:
                raise serializers.ValidationError('Be specify fb_token or ig_token')

    def to_representation(self, account):
        print("hogehoge", type(account))
        output = super().to_representation(account)
        try:
            token = Token.objects.get(user=account.user)
        except Token.DoesNotExist:
            token = Token(user=account.user)
            token.save()
        output['token'] = token.key
        print(output)
        return output






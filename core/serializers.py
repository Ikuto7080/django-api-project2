from django.contrib.auth.models import User
from rest_framework import serializers
from core.models import Account, ALLPost, GooglePlace, Post, PostImage, Profile
import uuid
import facebook
import requests
from instagram_basic_display.InstagramBasicDisplay import InstagramBasicDisplay
from rest_framework.authtoken.models import Token
from core.tasks import get_ig_post, get_fb_post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'first_name', 'last_name', 'email', 'is_staff']



class AccountSerializer(serializers.ModelSerializer):
    fb_code = serializers.CharField(required=False, write_only=True)
    ig_code = serializers.CharField(required=False, write_only=True)
    user = UserSerializer(read_only=True)
    redirect_uri = serializers.URLField(required=False, write_only=True)
    follow_line_id = serializers.CharField(required=False, write_only=True)
    class Meta:
        model = Account
        fields = ['id', 'user', 'fb_token' , 'ig_token', 'fb_code', 'ig_code', 'fb_id', 'ig_id', 'redirect_uri', 'line_user_id', 'follow_line_id', 'profile_picture']
        read_only_fields = ['user', 'fb_token', 'ig_token', 'fb_id', 'ig_id', 'profile_picture']

    def create(self, validated_data):
          fb_code = validated_data.get("fb_code")
          ig_code = validated_data.get("ig_code")
          redirect_uri = validated_data.get("redirect_uri", "https://localhost:8080/insta/")
          line_user_id = validated_data.get("line_user_id")
          follow_line_id = validated_data.get("follow_line_id")

          if fb_code:
                url = "https://graph.facebook.com/v9.0/oauth/access_token"
                params = {
                'client_id': '420945845838455',
                'redirect_uri': redirect_uri,
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
                if not account and line_user_id:
                    account = Account.objects.filter(line_user_id=line_user_id).first()
                    if account and not account.fb_id:
                        account.fb_id = fb_id
                        account.fb_token = fb_token
                        get_fb_post.delay(account.id)
                        account.save()

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
                account.line_user_id = line_user_id
                account.save()
                get_fb_post.delay(account.id)
                if follow_line_id:
                    follow_account = Account.objects.filter(line_user_id=follow_line_id).first()
                    follow_account.user.profile.friends.add(account.user)
                return account

          elif ig_code:
              #128183525822395, 7c0f1ebb5832df8f18b09bcd5ddbc133
                instagram_basic_display = InstagramBasicDisplay(app_id ='909807339845904', app_secret='f095f16729ea435ff0c36d6fda438d83', redirect_url= redirect_uri)
                auth_token = instagram_basic_display.get_o_auth_token(ig_code)
                instagram_basic_display.set_access_token(auth_token['access_token'])
                ig_profile = instagram_basic_display.get_user_profile()
                ig_id = ig_profile['id']
                account = Account.objects.filter(ig_id=ig_id).first()
                if not account and line_user_id:
                    account = Account.objects.filter(line_user_id=line_user_id).first()
                    if account and not account.ig_id:
                        account.ig_id = ig_id
                        account.ig_token = auth_token['access_token']
                        get_ig_post.delay(account.id)
                        account.save()
                if account:
                      return account 
                user = User(username=str(uuid.uuid4()))
                user.first_name = ig_profile['username']
                user.save()
                account = Account()
                account.user = user
                account.ig_id = ig_profile['id']
                account.ig_token = auth_token['access_token']
                account.line_user_id = line_user_id
                account.save()
                get_ig_post.delay(account.id)
                if follow_line_id:
                    follow_account = Account.objects.filter(line_user_id=follow_line_id).first()
                    follow_account.user.profile.friends.add(account.user)
                return account
                
          else:
                raise serializers.ValidationError('Be specify fb_token or ig_token')

    def to_representation(self, account):
        output = super().to_representation(account)
        try:
            token = Token.objects.get(user=account.user)
        except Token.DoesNotExist:
            token = Token(user=account.user)
            token.save()
        output['token'] = token.key
        return output

    # def update(self, )

class ALLPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ALLPost
        fields = ['id', 'user', 'media_url', 'post_url', 'latitude', 'longitude', 'location_name', 'fb_permalink', 'ig_permalink', 'image', 'google_info', 'place_id', 'location_id', 'message']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    friends = UserSerializer(many=True)
    profile_picture = serializers.CharField(source='user.account.profile_picture')
    class Meta:
        model = Profile
        fields = ['id', 'user', 'friends', 'profile_picture']
        

class GooglePlaceSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = GooglePlace
        fields = ['id', 'info', 'place_id', 'latitude', 'longitude','image']
    
    def get_image(self, obj):
        post_image = PostImage.objects.filter(post__google_place=obj).order_by('-id').first()
        if not post_image:
            return ''
        return post_image.url

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'url']



class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(source='postimage_set', many=True)
    user = UserSerializer(read_only=True)
    google_place = GooglePlaceSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'google_place', 'type', 'permalink', 'message', 'createdtime', 'ig_id', 'images', 'categories', 'city', 'state']


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_staff']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'categories']

class CityStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'city', 'state']
        








from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from core.models import Account, Device, GooglePlace, Post, PostImage, Profile, Device
import uuid
from django.core.files import File
from urllib import request
import facebook
import requests
from instagram_basic_display.InstagramBasicDisplay import InstagramBasicDisplay
from rest_framework.authtoken.models import Token
from core.tasks import get_ig_post, get_fb_post, send_notification


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'url', 'first_name', 'last_name', 'email', 'is_staff', 'profile_picture']

    def get_profile_picture(self, user):
        request = self.context.get('request')

        if not hasattr(user, 'account'):
            return ""
        if not user.account.profile_picture:
            return ""
        profile_picture = user.account.profile_picture.url
        return request.build_absolute_uri(profile_picture)



class PublicUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'profile_picture']

    def get_profile_picture(self, user):
        request = self.context.get('request')
        if not hasattr(user, 'account'):
            return ""
        if not user.account.profile_picture:
            return ""
        profile_picture = user.account.profile_picture.url
        print(profile_picture)
        return request.build_absolute_uri(profile_picture)


class ProfileSerializer(serializers.ModelSerializer):
    my_user_id = serializers.CharField(required=False, write_only=True)
    follow_user_id = serializers.CharField(required=False, write_only=True)
    unfollow_user_id = serializers.CharField(required=False, write_only=True)
    user = UserSerializer(read_only=True)
    followings = UserSerializer(many=True, read_only=True)
    fb_friends = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'my_user_id', 'follow_user_id' ,'unfollow_user_id' ,'user', 'followings', 'fb_friends']

    def create(self, validated_data):
        my_user_id = validated_data.get("my_user_id")
        follow_user_id = validated_data.get("follow_user_id")
        unfollow_user_id = validated_data.get("unfollow_user_id")
        if follow_user_id:
            my_user = User.objects.filter(id=my_user_id).first()
            follow_user = User.objects.filter(id=follow_user_id).first()
            my_user.profile.followings.add(follow_user)
            return {my_user, "=> ", follow_user}

        elif unfollow_user_id:
            print("unfollow user id", unfollow_user_id)
            my_user = User.objects.filter(id=my_user_id).first()
            unfollow_user = User.objects.filter(id=unfollow_user_id).first()
            my_user.profile.followings.remove(unfollow_user)
            return {my_user, "=> ", unfollow_user}


class InviterAccountSerializer(serializers.ModelSerializer):
    inviter = UserSerializer(source='account.inviter.user')
    class Meta:
        model = Account
        fields = ['inviter']

class AccountSerializer(serializers.ModelSerializer):
    fb_code = serializers.CharField(required=False, write_only=True)
    fb_access_token = serializers.CharField(required=False, write_only=True)
    ig_code = serializers.CharField(required=False, write_only=True)
    account_id = serializers.CharField(required=False,write_only=True)
    follow_account_id = serializers.CharField(required=False, write_only=True)
    user = UserSerializer(read_only=True)
    inviter = UserSerializer(source='inviter.user', read_only=True)
    redirect_uri = serializers.URLField(required=False, write_only=True)
    postkit_url = serializers.URLField(required=False, write_only=True)

    class Meta:
        model = Account
        fields = ['id', 'user', 'fb_token' , 'ig_token', 'fb_code', 'ig_code', 'fb_id', 'ig_id', 'redirect_uri', 'profile_picture', 'account_id', 'follow_account_id', 'inviter', 'fb_access_token', 'postkit_url']
        read_only_fields = ['user', 'fb_token', 'ig_token', 'fb_id', 'ig_id', 'inviter']

    def update(self, instance, validated_data):
        print('update: ', validated_data, instance)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        fb_code = validated_data.get("fb_code")
        ig_code = validated_data.get("ig_code")
        fb_access_token = validated_data.get("fb_access_token")
        account_id = validated_data.get("account_id")
        follow_account_id = validated_data.get("follow_account_id")
        redirect_uri = validated_data.get("redirect_uri", "https://localhost:8080/insta/")

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
            get_fb_post.delay(account.id)
            if follow_account_id:
                print("follow_account_id: ", follow_account_id)
                follow_account = Account.objects.filter(id=follow_account_id).first()
                follow_account.user.profile.followings.add(account.user)
                account.user.profile.followings.add(follow_account.user)
                account.inviter = follow_account
                account.save()
                is_fb_friend = graph.get_object("me/friends/" + str(follow_account.fb_id))
                print("is_fb_friend:  ", is_fb_friend)
                try:
                    friends = is_fb_friend["data"][0]
                    print(friends)
                    user.profile.fb_friends.add(follow_account.user)
                    follow_account.user.profile.fb_friends.add(user)
                except:
                    return ""
                send_notification.delay(account.id, follow_account_id)
            return account

        elif fb_access_token:
                fb_token = fb_access_token
                token = fb_token
                graph = facebook.GraphAPI(token)
                #fields = ['first_name', 'location{location}','email','link']
                profile = graph.get_object('me', fields='first_name, last_name, location,link,email')
                #Accountが存在するか確認する
                fb_id = profile['id'] 
                account = Account.objects.filter(fb_id=fb_id).first()
                # print('account: ' + str(account))
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
                # print('user: ' + str(user))
                account.save()
                get_fb_post.delay(account.id)
                if follow_account_id:
                    # this account invite you
                    follow_account = Account.objects.filter(id=follow_account_id).first()
                    follow_account.user.profile.friends.add(account.user)
                    account.user.profile.friends.add(follow_account.user)
                    account.inviter = follow_account
                    account.save()
                    send_notification.delay(account.id, follow_account_id)
                return account
            

        elif ig_code:
            instagram_basic_display = InstagramBasicDisplay(app_id ='909807339845904', app_secret='f095f16729ea435ff0c36d6fda438d83', redirect_url= redirect_uri)
            auth_token = instagram_basic_display.get_o_auth_token(ig_code)
            instagram_basic_display.set_access_token(auth_token['access_token'])
            ig_profile = instagram_basic_display.get_user_profile()
            ig_id = ig_profile['id']
            account = Account.objects.filter(id=account_id).first()
            account.ig_id = ig_id
            account.ig_token = auth_token['access_token']
            account.save()
            # get_ig_post(account.id)
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



class PublicAccountSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)
    class Meta:
        model = Account
        fields = ['id', 'user']

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
        fields = ['id', 'url', 'image']



class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(source='postimage_set', many=True)
    user = UserSerializer(read_only=True)
    google_place = GooglePlaceSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'google_place', 'type', 'permalink', 'message', 'createdtime', 'ig_id', 'fb_id','images', 'categories', 'city', 'state']

class PublicPostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(source='postimage_set', many=True)
    user = PublicUserSerializer(read_only=True)
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
        fields = ['categories']

class CityStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'city', 'state']

class DeviceSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    class Meta:
        model = Device
        fields = ['id', 'account', 'fcm_token']

    def create(self, validated_data):
        validated_data['account'] = Account.objects.get(user=self.context['request'].user)
        return super().create(validated_data)


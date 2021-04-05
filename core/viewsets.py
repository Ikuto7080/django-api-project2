from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, response, pagination
from rest_framework.permissions import AllowAny
from core.serializers import UserSerializer, AccountSerializer, ALLPostSerializer, GooglePlaceSerializer, PostSerializer, ProfileSerializer
from core.models import Account, ALLPost, GooglePlace, Post, Profile
from django.db.models import Q
from rest_framework.decorators import action

class MyPagenation(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permissions_classes = [AllowAny]

    # def get_queryset(self):
    #     queryset = self.queryset.filter(user=self.request.user.id)
    #     return queryset






class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
   
    
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]

class ALLPostViewSet(viewsets.ModelViewSet):
    queryset = ALLPost.objects.all()
    serializer_class = ALLPostSerializer
    permissions_classes = [permissions.AllowAny()]

class GooglePlaceViewSet(viewsets.ModelViewSet):
    queryset = GooglePlace.objects.all()
    serializer_class = GooglePlaceSerializer
    permissions_classes = [permissions.AllowAny()]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        google_place = self.request.query_params.get('google_place')
        if google_place is not None:
             queryset = self.queryset.filter(google_place=google_place)
        return queryset


        print(id)
        return queryset


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        #filtering with user_id
        if user_id is not None:
            queryset = self.queryset.filter(user_id=user_id)
            return queryset
        #filtering with user_ids filter
        user_ids = self.request.query_params.get('user_ids')
        if user_ids is not None:
            user_id = user_ids.split(',')
            queryset = self.queryset.filter(
                #__inのあとはリスト型じゃないといけない
                user_id__in=user_id
                )
            return queryset
        google_place = self.request.query_params.get('google_place')
        #filtering with google_place filter
        if google_place is not None:
             queryset = self.queryset.filter(google_place=google_place)
             return queryset
        categories = self.request.query_params.get('categories')
        if categories is not None:
            queryset = self.queryset.filter(categories=categories)
            return queryset
        queryset = self.queryset.filter(Q(user=self.request.user) | Q(user__in=self.request.user.profile.friends.all()))
        return queryset


class FollowingsViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyPagenation

    def get_queryset(self):
        friend_ids = [f.id for f in self.request.user.profile.friends.all()]
        #__in...IN句検索
        return self.queryset.filter(user_id__in=friend_ids)
        # return self.request.user.profile.friends.all()

    @action(detail=False, methods=['get'])
    def count(self, request):
        followings_count = request.user.profile.friends.count()
        body = {'count': followings_count}
        return response.Response(body)


class FollowersViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyPagenation


    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(friends__in=[user])

    @action(detail=False, methods=['get'])
    def count(self, request):
        followers_count = self.queryset.filter(friends__in=[request.user]).count()
        body = {'count': followers_count}
        return response.Response(body)





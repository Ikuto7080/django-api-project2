from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from core.serializers import UserSerializer, AccountSerializer, ALLPostSerializer, GooglePlaceSerializer, PostSerializer, ProfileSerializer, RelationshipSerialzier
from core.models import Account, ALLPost, GooglePlace, Post, Profile, Relationship



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

class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerialzier
    permissions_classes = [permissions.AllowAny()]





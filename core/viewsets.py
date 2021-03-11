from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from core.serializers import UserSerializer, AccountSerializer, FbPostSerializer, IgPostSerializer
from core.models import Account, FbPost, IgPost



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]
   
    
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        else:
            return [permissions.IsAuthenticated()]

class FbPostViewSet(viewsets.ModelViewSet):
    queryset = FbPost.objects.all()
    serializer_class = FbPostSerializer
    permissions_classes = [AllowAny]

class IgPostViewSet(viewsets.ModelViewSet):
    queryset = IgPost.objects.all()
    serializer_class = IgPostSerializer
    permissions_classes = [AllowAny]




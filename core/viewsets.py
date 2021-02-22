from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from core.serializers import UserSerializer, AccountSerializer
from core.models import Account



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        else:
            return [permissions.IsAuthenticated()]






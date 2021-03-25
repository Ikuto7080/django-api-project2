from core.models import Profile
from core.serializers import ProfileSerializer
from rest_framework import generics


class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        print(user)
        return Profile.objects.filter(user=user)


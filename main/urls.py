from django.conf.urls import url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static



from rest_framework import routers
from core.viewsets import UserViewSet, AccountViewSet, GooglePlaceViewSet, PostViewSet, ProfileViewSet, FeedViewSet, FollowingsViewSet, FollowersViewSet, CategoriesViewSet, CityStateViewSet

from core.filters import ProfileList
from core.views import LineWebHookView
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'restaurants', GooglePlaceViewSet)
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'profiles', ProfileViewSet)
router.register(r'feeds', FeedViewSet, basename='feeds')
router.register(r'followings', FollowingsViewSet, basename='followings')
router.register(r'followers', FollowersViewSet, basename = 'followers')
router.register(r'categories', CategoriesViewSet)
router.register(r'citystates', CityStateViewSet, basename='citystates')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    path('line-webhook/', LineWebHookView.as_view()),
    path('profile-list/', ProfileList.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
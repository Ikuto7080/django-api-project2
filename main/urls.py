"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static



from rest_framework import routers
from core.viewsets import UserViewSet, AccountViewSet, ALLPostViewSet, GooglePlaceViewSet, PostViewSet, ProfileViewSet, FeedViewSet, FollowingsViewSet, FollowersViewSet, CategoriesViewSet, CityStateViewSet

from core.filters import ProfileList
from core.views import LineWebHookView
from django.urls import path, include



router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'allposts', ALLPostViewSet)
router.register(r'restaurants', GooglePlaceViewSet)
router.register(r'posts', PostViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'feeds', FeedViewSet, basename='feeds')
router.register(r'followings', FollowingsViewSet, basename='followings')
router.register(r'followers', FollowersViewSet, basename = 'followers')
router.register(r'categories', CategoriesViewSet)
router.register(r'citystates', CityStateViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    path('line-webhook/', LineWebHookView.as_view()),
    path('profile-list/', ProfileList.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


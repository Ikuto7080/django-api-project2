from django.contrib import admin
from core.models import Account, GooglePlace, IgLocation, Post, PostImage, Profile, FoursquareVenue


class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'fb_id']
    

admin.site.register(Account, AccountAdmin)
admin.site.register(GooglePlace)
admin.site.register(IgLocation)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Profile)
admin.site.register(FoursquareVenue)




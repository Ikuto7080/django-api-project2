from django.contrib import admin
from core.models import Account, FbPost, IgPost, MediaPost


class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'fb_id']
    

admin.site.register(Account, AccountAdmin)
admin.site.register(FbPost)
admin.site.register(IgPost)
admin.site.register(MediaPost)


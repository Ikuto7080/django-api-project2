from django.contrib import admin
from core.models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'fb_id']
    

admin.site.register(Account, AccountAdmin)


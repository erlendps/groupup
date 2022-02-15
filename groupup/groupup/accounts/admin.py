from django.contrib import admin

from .models import GroupUpUser, UserGroup, Interest

admin.site.register(GroupUpUser)
admin.site.register(UserGroup)
admin.site.register(Interest)

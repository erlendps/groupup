from django.contrib import admin

from .models import GroupUpUser, UserGroup, Interest, Reviews

admin.site.register(GroupUpUser)
admin.site.register(UserGroup)
admin.site.register(Interest)
admin.site.register(Reviews)

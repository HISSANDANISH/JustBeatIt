from django.contrib import admin

# Register your models here.
from . models import Profile, FriendRequest

admin.site.register(Profile)
admin.site.register(FriendRequest)
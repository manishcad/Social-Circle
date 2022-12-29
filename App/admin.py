from django.contrib import admin
from .models import Profile, Post, Like, Followers_Model, Chat
# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Followers_Model)
admin.site.register(Chat)

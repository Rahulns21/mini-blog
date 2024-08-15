from django.contrib import admin
from .models import Post, UserProfile, Category, Comment

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Comment)
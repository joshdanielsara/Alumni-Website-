from django.contrib import admin

# Register your models here.
# myapp/admin.py
from django.contrib import admin
from .models import Post, Like, Comment

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
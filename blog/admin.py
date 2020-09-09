from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Post, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment, MPTTModelAdmin)
from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'created_at', 'image', 'user']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'created_at', 'user', 'post']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

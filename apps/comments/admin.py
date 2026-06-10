from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'parent', 'like_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username', 'project__title']
    readonly_fields = ['created_at', 'like_count']

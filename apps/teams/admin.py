from django.contrib import admin
from .models import TeamPosition, Application

@admin.register(TeamPosition)
class TeamPositionAdmin(admin.ModelAdmin):
    list_display = ['project', 'role', 'is_open', 'created_at']
    list_filter = ['is_open']
    search_fields = ['project__title', 'role']
    list_editable = ['is_open']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['user__username', 'position__role', 'position__project__title']
    list_editable = ['status']
    readonly_fields = ['created_at']

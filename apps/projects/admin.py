from django.contrib import admin
from .models import Project, ProjectScreenshot

class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'category', 'status', 'featured', 'vote_count', 'views', 'created_at']
    list_filter = ['status', 'featured', 'category']
    search_fields = ['title', 'tagline', 'owner__username']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'featured']
    inlines = [ProjectScreenshotInline]
    readonly_fields = ['views', 'created_at', 'vote_count', 'comment_count', 'trending_score']
    
    def vote_count(self, obj):
        return obj.vote_count
    vote_count.short_description = 'Votes'

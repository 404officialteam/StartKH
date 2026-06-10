from django.db import models
from apps.projects.models import Project

class ProjectAnalytics(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='analytics_logs')
    date = models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    website_clicks = models.PositiveIntegerField(default=0)
    github_clicks = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('project', 'date')
        verbose_name_plural = "Project Analytics"

    def __str__(self):
        return f"{self.project.title} Analytics - {self.date}"

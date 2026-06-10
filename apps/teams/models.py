from django.db import models
from django.contrib.auth.models import User
from apps.projects.models import Project

class TeamPosition(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='positions')
    role = models.CharField(max_length=100, help_text="e.g. Developer, Designer, Marketer")
    description = models.TextField()
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} at {self.project.title}"

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    position = models.ForeignKey(TeamPosition, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_applications')
    message = models.TextField(help_text="Introduce yourself and explain why you are a good fit")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('position', 'user')

    def __str__(self):
        return f"{self.user.username} application for {self.position.role}"

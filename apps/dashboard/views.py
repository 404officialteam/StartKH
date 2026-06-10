from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.projects.models import Project
from apps.teams.models import Application
from apps.notifications.models import Notification

@login_required
def user_dashboard_view(request):
    my_projects = Project.objects.filter(owner=request.user)
    
    # Get all applications sent to the user's projects
    incoming_applications = Application.objects.filter(position__project__owner=request.user).order_by('-created_at')
    
    # Get all applications sent by the user to other projects
    my_applications = Application.objects.filter(user=request.user).order_by('-created_at')
    
    recent_notifications = Notification.objects.filter(user=request.user)[:10]
    
    context = {
        'my_projects': my_projects,
        'incoming_applications': incoming_applications,
        'my_applications': my_applications,
        'recent_notifications': recent_notifications
    }
    return render(request, 'dashboard/home.html', context)

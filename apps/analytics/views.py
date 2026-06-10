from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.projects.models import Project
from apps.votes.models import Vote
from apps.comments.models import Comment
from .models import ProjectAnalytics
from django.db.models import Sum

@login_required
def analytics_dashboard_view(request):
    user_projects = Project.objects.filter(owner=request.user)
    
    # Aggregated metrics
    total_views = user_projects.aggregate(Sum('views'))['views__sum'] or 0
    
    total_votes = Vote.objects.filter(project__owner=request.user).count()
    total_comments = Comment.objects.filter(project__owner=request.user).count()
    
    # Detailed analytics logs for charting
    analytics_logs = ProjectAnalytics.objects.filter(project__owner=request.user).order_by('-date')[:30]
    
    context = {
        'projects': user_projects,
        'total_views': total_views,
        'total_votes': total_votes,
        'total_comments': total_comments,
        'analytics_logs': analytics_logs
    }
    return render(request, 'analytics/dashboard.html', context)

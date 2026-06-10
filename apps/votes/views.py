from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.projects.models import Project
from .models import Vote
from apps.notifications.utils import create_notification

@login_required
def toggle_vote_view(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        vote_query = Vote.objects.filter(user=request.user, project=project)
        
        if vote_query.exists():
            vote_query.delete()
            voted = False
            message = "Upvote removed"
        else:
            Vote.objects.create(user=request.user, project=project)
            voted = True
            message = "Project upvoted"
            
            # Send notification to project owner
            if project.owner != request.user:
                create_notification(
                    user=project.owner,
                    title="🔥 New Upvote!",
                    message=f"{request.user.username} upvoted your project '{project.title}'",
                    link=f"/project/{project.slug}/"
                )
                
        return JsonResponse({
            'status': 'success',
            'voted': voted,
            'vote_count': project.vote_count,
            'message': message
        })
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

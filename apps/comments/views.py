from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.projects.models import Project
from .models import Comment
from apps.notifications.utils import create_notification
import re

@login_required
def add_comment_view(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        content = request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent_id')
        
        if not content:
            messages.error(request, "Comment content cannot be empty.")
            return redirect('project_detail', slug=project.slug)
            
        parent = None
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id)

        comment = Comment.objects.create(
            user=request.user,
            project=project,
            content=content,
            parent=parent
        )

        # Notify project owner
        if project.owner != request.user:
            create_notification(
                user=project.owner,
                title="💬 New Comment",
                message=f"{request.user.username} commented on your project '{project.title}'",
                link=f"/project/{project.slug}/"
            )

        # Notify parent comment author if reply
        if parent and parent.user != request.user:
            create_notification(
                user=parent.user,
                title="💬 New Reply",
                message=f"{request.user.username} replied to your comment on '{project.title}'",
                link=f"/project/{project.slug}/"
            )

        # Parse mentions e.g. @username and notify mentioned users
        mentions = re.findall(r'@(\w+)', content)
        from django.contrib.auth.models import User
        for username in set(mentions):
            try:
                mentioned_user = User.objects.get(username=username)
                if mentioned_user != request.user and mentioned_user != project.owner and (not parent or mentioned_user != parent.user):
                    create_notification(
                        user=mentioned_user,
                        title="🔔 You were mentioned",
                        message=f"{request.user.username} mentioned you in a comment on '{project.title}'",
                        link=f"/project/{project.slug}/"
                    )
            except User.DoesNotExist:
                pass

        messages.success(request, "Your comment has been added!")
        return redirect('project_detail', slug=project.slug)

    return redirect('explore')

@login_required
def toggle_like_comment_view(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            liked = False
        else:
            comment.likes.add(request.user)
            liked = True
            
            # Notify comment author of like
            if comment.user != request.user:
                create_notification(
                    user=comment.user,
                    title="👍 Comment Liked",
                    message=f"{request.user.username} liked your comment on '{comment.project.title}'",
                    link=f"/project/{comment.project.slug}/"
                )
                
        return JsonResponse({
            'status': 'success',
            'liked': liked,
            'like_count': comment.like_count
        })
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

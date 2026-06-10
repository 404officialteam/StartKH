from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.projects.models import Project
from .models import TeamPosition, Application
from apps.notifications.utils import create_notification

@login_required
def create_position_view(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug, owner=request.user)
    
    if request.method == 'POST':
        role = request.POST.get('role', '').strip()
        description = request.POST.get('description', '').strip()
        
        if not role or not description:
            messages.error(request, "Role and description cannot be empty.")
            return redirect('project_detail', slug=project.slug)
            
        TeamPosition.objects.create(
            project=project,
            role=role,
            description=description
        )
        messages.success(request, f"Recruiting position for '{role}' has been added!")
        return redirect('project_detail', slug=project.slug)

    return redirect('project_detail', slug=project.slug)

@login_required
def apply_position_view(request, position_id):
    position = get_object_or_404(TeamPosition, id=position_id, is_open=True)
    
    # Check if already applied
    if Application.objects.filter(position=position, user=request.user).exists():
        messages.warning(request, "You have already applied for this position.")
        return redirect('project_detail', slug=position.project.slug)

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        if not message:
            messages.error(request, "Application message cannot be empty.")
            return redirect('project_detail', slug=position.project.slug)
            
        Application.objects.create(
            position=position,
            user=request.user,
            message=message
        )
        
        # Notify project owner
        create_notification(
            user=position.project.owner,
            title="🤝 New Position Application",
            message=f"{request.user.username} applied to recruit as {position.role} for '{position.project.title}'",
            link=f"/project/{position.project.slug}/"
        )
        
        messages.success(request, "Your application has been submitted successfully!")
        return redirect('project_detail', slug=position.project.slug)

    return render(request, 'teams/apply.html', {'position': position})

@login_required
def update_application_status_view(request, application_id):
    application = get_object_or_404(Application, id=application_id, position__project__owner=request.user)
    
    if request.method == 'POST':
        status = request.POST.get('status') # accepted or rejected
        if status in ['accepted', 'rejected']:
            application.status = status
            application.save()
            
            # Notify applicant
            create_notification(
                user=application.user,
                title="🤝 Application Update",
                message=f"Your application for {application.position.role} at '{application.position.project.title}' has been {status}!",
                link=f"/project/{application.position.project.slug}/"
            )
            
            messages.success(request, f"Application has been {status}!")
            
    return redirect('project_detail', slug=application.position.project.slug)

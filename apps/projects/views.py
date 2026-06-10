from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from .models import Project, ProjectScreenshot
from .forms import ProjectForm
from apps.categories.models import Category
from apps.votes.models import Vote
from apps.comments.models import Comment
from apps.teams.models import TeamPosition
from apps.analytics.models import ProjectAnalytics

def explore_view(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    time_filter = request.GET.get('time', 'all') # today, weekly, monthly, all

    projects = Project.objects.filter(status='approved')

    # Apply category filter
    if category_slug:
        projects = projects.filter(category__slug=category_slug)

    # Apply search query
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(tagline__icontains=query) |
            Q(description__icontains=query) |
            Q(owner__username__icontains=query)
        )

    # Apply time filter for trending
    now = timezone.now()
    if time_filter == 'today':
        projects = projects.filter(created_at__gte=now - timedelta(days=1))
    elif time_filter == 'weekly':
        projects = projects.filter(created_at__gte=now - timedelta(weeks=1))
    elif time_filter == 'monthly':
        projects = projects.filter(created_at__gte=now - timedelta(days=30))

    # Rank projects: Sort by trending score (Votes, comments, views)
    # We can pre-sort them in Python to make it simpler and accurate to our trending property
    project_list = list(projects)
    project_list.sort(key=lambda p: p.trending_score, reverse=True)

    categories = Category.objects.all()

    # Find out which projects the current user has upvoted
    user_votes = []
    if request.user.is_authenticated:
        user_votes = Vote.objects.filter(user=request.user).values_list('project_id', flat=True)

    context = {
        'projects': project_list,
        'categories': categories,
        'selected_category': category_slug,
        'selected_time': time_filter,
        'query': query,
        'user_votes': user_votes
    }
    return render(request, 'projects/explore.html', context)

def project_detail_view(request, slug):
    project = get_object_or_404(Project, slug=slug, status='approved')
    
    # Increment views
    project.views += 1
    project.save(update_fields=['views'])

    # Track daily analytics
    try:
        analytics, created = ProjectAnalytics.objects.get_or_create(project=project, date=timezone.now().date())
        analytics.views += 1
        analytics.save(update_fields=['views'])
    except Exception:
        pass

    # Threaded Comments (only root comments first, replies are loaded nested)
    comments = Comment.objects.filter(project=project, parent=None).order_by('-created_at')
    
    # Team positions
    positions = TeamPosition.objects.filter(project=project, is_open=True)

    # Check if current user voted
    has_voted = False
    if request.user.is_authenticated:
        has_voted = Vote.objects.filter(user=request.user, project=project).exists()

    context = {
        'project': project,
        'comments': comments,
        'positions': positions,
        'has_voted': has_voted
    }
    return render(request, 'projects/project_detail.html', context)

@login_required
def project_create_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()

            # Handle screenshots
            files = request.FILES.getlist('screenshots')
            for f in files:
                ProjectScreenshot.objects.create(project=project, image=f)

            messages.success(request, f"Project '{project.title}' has been launched successfully!")
            return redirect('project_detail', slug=project.slug)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_create.html', {'form': form})

@login_required
def project_update_view(request, slug):
    project = get_object_or_404(Project, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            
            # Handle additional screenshots if uploaded
            files = request.FILES.getlist('screenshots')
            for f in files:
                ProjectScreenshot.objects.create(project=project, image=f)

            messages.success(request, f"Project '{project.title}' has been updated!")
            return redirect('project_detail', slug=project.slug)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_update.html', {'form': form, 'project': project})

@login_required
def project_delete_view(request, slug):
    project = get_object_or_404(Project, slug=slug, owner=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Your project has been deleted.")
        return redirect('project_manage')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})

@login_required
def project_manage_view(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'projects/project_manage.html', {'projects': projects})

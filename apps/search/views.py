from django.shortcuts import render
from django.db.models import Q
from apps.projects.models import Project
from django.contrib.auth.models import User

def search_results_view(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    tech = request.GET.get('tech', '').strip()
    location = request.GET.get('location', '').strip()
    
    results = Project.objects.filter(status='approved')
    
    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(tagline__icontains=query) |
            Q(description__icontains=query) |
            Q(owner__username__icontains=query)
        )
        
    if category:
        results = results.filter(category__name__icontains=category)
        
    if tech:
        # Search by skills/technologies from owner profiles or taglines
        results = results.filter(
            Q(owner__profile__skills__icontains=tech) |
            Q(tagline__icontains=tech) |
            Q(description__icontains=tech)
        )
        
    if location:
        results = results.filter(owner__profile__location__icontains=location)
        
    context = {
        'results': results,
        'query': query,
        'category': category,
        'tech': tech,
        'location': location
    }
    return render(request, 'search/results.html', context)

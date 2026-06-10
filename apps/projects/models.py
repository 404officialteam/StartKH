from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from apps.categories.models import Category

class Project(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='projects')
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    logo = models.ImageField(upload_to='logos/', default='logos/default.png', blank=True)
    cover_image = models.ImageField(upload_to='covers/', default='covers/default-project.png', blank=True)
    tagline = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    video_demo = models.URLField(blank=True, help_text="YouTube or Video link")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='approved') # default approved for easy developer testing
    featured = models.BooleanField(default=False)
    featured_date = models.DateTimeField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            # Make slug unique
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def vote_count(self):
        return self.votes.count()

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def trending_score(self):
        # Trending Score = Upvotes * 15 + Comments * 5 + Views
        return (self.vote_count * 15) + (self.comment_count * 5) + self.views

class ProjectScreenshot(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='screenshots/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Screenshot for {self.project.title}"

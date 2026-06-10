from django.urls import path
from . import views

urlpatterns = [
    path('toggle/<int:project_id>/', views.toggle_vote_view, name='toggle_vote'),
]

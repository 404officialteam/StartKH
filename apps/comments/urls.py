from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:project_id>/', views.add_comment_view, name='add_comment'),
    path('like/<int:comment_id>/', views.toggle_like_comment_view, name='like_comment'),
]

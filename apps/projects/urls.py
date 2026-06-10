from django.urls import path
from . import views

urlpatterns = [
    path('', views.explore_view, name='explore'),
    path('project/create/', views.project_create_view, name='project_create'),
    path('project/manage/', views.project_manage_view, name='project_manage'),
    path('project/<slug:slug>/', views.project_detail_view, name='project_detail'),
    path('project/<slug:slug>/edit/', views.project_update_view, name='project_update'),
    path('project/<slug:slug>/delete/', views.project_delete_view, name='project_delete'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('position/create/<slug:project_slug>/', views.create_position_view, name='create_position'),
    path('apply/<int:position_id>/', views.apply_position_view, name='apply_position'),
    path('application/status/<int:application_id>/', views.update_application_status_view, name='update_application_status'),
]

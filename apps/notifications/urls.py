from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_notifications_view, name='notifications_list'),
    path('read/<int:notification_id>/', views.mark_read_view, name='mark_notification_read'),
]

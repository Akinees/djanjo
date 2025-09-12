from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('<int:notification_id>/read/', views.mark_as_read, name='mark_read'),
    path('count/', views.unread_count, name='unread_count'),
    path('preferences/', views.preferences, name='preferences'),
]
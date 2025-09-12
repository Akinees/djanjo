from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('detailed/', views.detailed_progress, name='detailed'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
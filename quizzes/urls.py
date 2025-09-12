from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.quiz_list, name='list'),
    path('<int:pk>/', views.quiz_detail, name='detail'),
    path('<int:pk>/take/', views.take_quiz, name='take'),
    path('results/<int:attempt_id>/', views.quiz_results, name='results'),
]
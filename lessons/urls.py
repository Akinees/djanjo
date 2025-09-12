from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.lesson_list, name='list'),
    path('<int:pk>/', views.lesson_detail, name='detail'),
    path('<int:pk>/complete/', views.mark_lesson_complete, name='complete'),
    path('category/<int:category_id>/', views.category_lessons, name='category'),
]
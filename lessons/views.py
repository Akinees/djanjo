from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Lesson, Category
from progress.models import LessonProgress

def lesson_list(request):
    lessons = Lesson.objects.select_related('category').all()
    categories = Category.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        lessons = lessons.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Category filter
    category_filter = request.GET.get('category', '')
    if category_filter:
        lessons = lessons.filter(category__pk=category_filter)
    
    # Difficulty filter
    difficulty_filter = request.GET.get('difficulty', '')
    if difficulty_filter:
        lessons = lessons.filter(difficulty=difficulty_filter)
    
    # Pagination
    paginator = Paginator(lessons, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'difficulty_filter': difficulty_filter,
        'difficulty_choices': Lesson.DIFFICULTY_CHOICES,
    }
    return render(request, 'lessons/list.html', context)

@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    
    # Get or create progress for this lesson
    progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'completed': False}
    )
    
    # Check if user has completed this lesson
    user_completed = progress.completed
    
    context = {
        'lesson': lesson,
        'user_completed': user_completed,
        'progress': progress,
    }
    return render(request, 'lessons/detail.html', context)

@login_required
def mark_lesson_complete(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    
    progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'completed': False}
    )
    
    if not progress.completed:
        progress.completed = True
        progress.save()
        
        # Award points to user
        request.user.total_points += lesson.points
        request.user.save()
        
        messages.success(request, f'Congratulations! You completed "{lesson.title}" and earned {lesson.points} points!')
    else:
        messages.info(request, 'You have already completed this lesson.')
    
    return redirect('lessons:detail', pk=pk)

def category_lessons(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    lessons = category.lessons.all()
    
    context = {
        'category': category,
        'lessons': lessons,
    }
    return render(request, 'lessons/category.html', context)
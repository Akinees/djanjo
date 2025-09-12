from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import LessonProgress, QuizProgress, UserStreak, LearningGoal
from lessons.models import Lesson, Category
from quizzes.models import QuizAttempt

@login_required
def dashboard(request):
    user = request.user
    
    # Lesson progress stats
    total_lessons = Lesson.objects.count()
    completed_lessons = LessonProgress.objects.filter(user=user, completed=True).count()
    progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    
    # Recent progress
    recent_lessons = LessonProgress.objects.filter(
        user=user, 
        completed=True
    ).select_related('lesson').order_by('-completed_at')[:5]
    
    # Quiz stats
    quiz_attempts = QuizAttempt.objects.filter(user=user)
    avg_quiz_score = quiz_attempts.aggregate(avg_score=Avg('percentage'))['avg_score'] or 0
    
    # Category progress
    categories = Category.objects.annotate(
        total_lessons=Count('lessons'),
        completed_lessons=Count('lessons__lessonprogress', 
                              filter=models.Q(lessons__lessonprogress__user=user, 
                                             lessons__lessonprogress__completed=True))
    )
    
    # Learning streak
    streak, created = UserStreak.objects.get_or_create(user=user)
    
    # Learning goals
    active_goals = LearningGoal.objects.filter(
        user=user, 
        completed=False,
        end_date__gte=timezone.now().date()
    )
    
    context = {
        'total_lessons': total_lessons,
        'completed_lessons': completed_lessons,
        'progress_percentage': progress_percentage,
        'recent_lessons': recent_lessons,
        'avg_quiz_score': avg_quiz_score,
        'categories': categories,
        'streak': streak,
        'active_goals': active_goals,
        'total_points': user.total_points,
    }
    return render(request, 'progress/dashboard.html', context)

@login_required
def detailed_progress(request):
    user = request.user
    
    # All lesson progress
    lesson_progress = LessonProgress.objects.filter(user=user).select_related('lesson', 'lesson__category')
    
    # All quiz progress
    quiz_progress = QuizProgress.objects.filter(user=user).select_related('quiz')
    
    # Monthly progress
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_completions = LessonProgress.objects.filter(
        user=user,
        completed=True,
        completed_at__gte=thirty_days_ago
    ).count()
    
    context = {
        'lesson_progress': lesson_progress,
        'quiz_progress': quiz_progress,
        'recent_completions': recent_completions,
    }
    return render(request, 'progress/detailed.html', context)

@login_required
def leaderboard(request):
    top_learners = User.objects.order_by('-total_points')[:20]
    user_rank = User.objects.filter(total_points__gt=request.user.total_points).count() + 1
    
    context = {
        'top_learners': top_learners,
        'user_rank': user_rank,
    }
    return render(request, 'progress/leaderboard.html', context)
from django.contrib import admin
from .models import LessonProgress, QuizProgress, UserStreak, LearningGoal

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'completed', 'completed_at', 'time_spent_minutes']
    list_filter = ['completed', 'completed_at', 'lesson__category']
    search_fields = ['user__username', 'lesson__title']

@admin.register(QuizProgress)
class QuizProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'best_percentage', 'attempts', 'passed', 'last_attempt_at']
    list_filter = ['passed', 'last_attempt_at']
    search_fields = ['user__username', 'quiz__title']

@admin.register(UserStreak)
class UserStreakAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_streak', 'longest_streak', 'last_activity_date']
    search_fields = ['user__username']

@admin.register(LearningGoal)
class LearningGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal_type', 'target_value', 'current_value', 'progress_percentage', 'completed']
    list_filter = ['goal_type', 'completed', 'start_date']
    search_fields = ['user__username']
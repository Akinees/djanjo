from django.contrib import admin
from .models import Quiz, Question, Answer, QuizAttempt, UserAnswer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'quiz_type', 'lesson', 'passing_score', 'points_reward', 'created_at']
    list_filter = ['quiz_type', 'created_at']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_text', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'quiz']
    search_fields = ['question_text']
    inlines = [AnswerInline]

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'percentage', 'passed', 'completed_at']
    list_filter = ['passed', 'quiz', 'completed_at']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['score', 'percentage', 'passed']
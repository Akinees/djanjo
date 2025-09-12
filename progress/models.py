from django.db import models
from django.contrib.auth import get_user_model
from lessons.models import Lesson
from quizzes.models import Quiz

User = get_user_model()

class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent_minutes = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'lesson')
        ordering = ['lesson__order', 'lesson__created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"

class QuizProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    best_score = models.PositiveIntegerField(default=0)
    best_percentage = models.FloatField(default=0)
    attempts = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'quiz')
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"

class UserStreak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.current_streak} days"

class LearningGoal(models.Model):
    GOAL_TYPES = [
        ('daily_lessons', 'Daily Lessons'),
        ('weekly_lessons', 'Weekly Lessons'),
        ('monthly_lessons', 'Monthly Lessons'),
        ('points', 'Points Target'),
        ('streak', 'Learning Streak'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_goals')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_value = models.PositiveIntegerField()
    current_value = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    
    def __str__(self):
        return f"{self.user.username} - {self.get_goal_type_display()}: {self.target_value}"
    
    @property
    def progress_percentage(self):
        if self.target_value == 0:
            return 0
        return min((self.current_value / self.target_value) * 100, 100)
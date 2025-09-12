from django import forms
from .models import Quiz, Question, Answer

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'lesson', 'quiz_type', 'time_limit_minutes', 'passing_score', 'points_reward']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
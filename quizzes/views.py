from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Count
from .models import Quiz, QuizAttempt, UserAnswer, Question
from .forms import QuizForm

def quiz_list(request):
    quizzes = Quiz.objects.annotate(
        avg_score=Avg('quizattempt__percentage'),
        attempt_count=Count('quizattempt')
    )
    
    context = {
        'quizzes': quizzes,
    }
    return render(request, 'quizzes/list.html', context)

@login_required
def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    user_attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by('-started_at')
    best_attempt = user_attempts.first() if user_attempts else None
    
    context = {
        'quiz': quiz,
        'user_attempts': user_attempts[:5],  # Show last 5 attempts
        'best_attempt': best_attempt,
        'can_retake': True,  # You can add logic here to limit retakes
    }
    return render(request, 'quizzes/detail.html', context)

@login_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.all()
    
    if request.method == 'POST':
        # Create quiz attempt
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            total_questions=questions.count()
        )
        
        correct_answers = 0
        total_points = 0
        
        for question in questions:
            answer_key = f'question_{question.id}'
            
            if question.question_type == 'multiple_choice':
                selected_answer_id = request.POST.get(answer_key)
                if selected_answer_id:
                    selected_answer = question.answers.get(id=selected_answer_id)
                    is_correct = selected_answer.is_correct
                    
                    UserAnswer.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_answer=selected_answer,
                        is_correct=is_correct
                    )
                    
                    if is_correct:
                        correct_answers += 1
                        total_points += question.points
            
            elif question.question_type == 'true_false':
                selected_answer_id = request.POST.get(answer_key)
                if selected_answer_id:
                    selected_answer = question.answers.get(id=selected_answer_id)
                    is_correct = selected_answer.is_correct
                    
                    UserAnswer.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_answer=selected_answer,
                        is_correct=is_correct
                    )
                    
                    if is_correct:
                        correct_answers += 1
                        total_points += question.points
            
            elif question.question_type == 'short_answer':
                text_answer = request.POST.get(answer_key, '').strip()
                correct_answer = question.answers.filter(is_correct=True).first()
                is_correct = False
                
                if correct_answer and text_answer.lower() == correct_answer.answer_text.lower():
                    is_correct = True
                    correct_answers += 1
                    total_points += question.points
                
                UserAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    text_answer=text_answer,
                    is_correct=is_correct
                )
        
        # Calculate final score
        percentage = (correct_answers / questions.count()) * 100 if questions.count() > 0 else 0
        passed = percentage >= quiz.passing_score
        
        attempt.score = correct_answers
        attempt.percentage = percentage
        attempt.passed = passed
        attempt.completed_at = timezone.now()
        attempt.save()
        
        # Award points if passed
        if passed:
            request.user.total_points += quiz.points_reward
            request.user.save()
            messages.success(request, f'Congratulations! You passed with {percentage:.1f}% and earned {quiz.points_reward} points!')
        else:
            messages.warning(request, f'You scored {percentage:.1f}%. You need {quiz.passing_score}% to pass. Try again!')
        
        return redirect('quizzes:results', attempt_id=attempt.id)
    
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quizzes/take.html', context)

@login_required
def quiz_results(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    user_answers = attempt.user_answers.select_related('question', 'selected_answer')
    
    context = {
        'attempt': attempt,
        'user_answers': user_answers,
    }
    return render(request, 'quizzes/results.html', context)
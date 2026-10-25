from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from quiz_app.models import Subject, Quiz, Question, QuizAttempt, UserAnswer


@login_required
def user_dashboard(request):
    user = request.user
    attempts = QuizAttempt.objects.filter(user=user)
    total_attempts = attempts.count()
    passed_attempts = attempts.filter(passed=True).count()
    avg_score = attempts.aggregate(avg=Avg('percentage'))['avg'] or 0.0
    
    # Recent attempts
    recent_attempts = attempts.select_related('quiz', 'quiz__subject')[:5]
    
    # Available subjects with published quizzes
    subjects = Subject.objects.annotate(
        published_quizzes_count=Count('quizzes', filter=Q(quizzes__is_published=True))
    ).filter(published_quizzes_count__gt=0)
    
    # Featured / Latest published quizzes
    featured_quizzes = Quiz.objects.filter(is_published=True).select_related('subject')[:6]

    context = {
        'total_attempts': total_attempts,
        'passed_attempts': passed_attempts,
        'pass_rate': round((passed_attempts / total_attempts * 100), 1) if total_attempts > 0 else 0,
        'avg_score': round(avg_score, 1),
        'recent_attempts': recent_attempts,
        'subjects': subjects,
        'featured_quizzes': featured_quizzes,
    }
    return render(request, 'user/dashboard.html', context)


@login_required
def quiz_list(request):
    subject_id = request.GET.get('subject')
    query = request.GET.get('q', '').strip()

    quizzes = Quiz.objects.filter(is_published=True).select_related('subject')
    
    if subject_id:
        quizzes = quizzes.filter(subject_id=subject_id)
    if query:
        quizzes = quizzes.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(subject__name__icontains=query))

    subjects = Subject.objects.all()
    selected_subject = None
    if subject_id:
        selected_subject = Subject.objects.filter(id=subject_id).first()

    context = {
        'quizzes': quizzes,
        'subjects': subjects,
        'selected_subject': selected_subject,
        'query': query,
    }
    return render(request, 'user/quiz_list.html', context)


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    past_attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz)
    best_attempt = past_attempts.order_by('-percentage').first()
    
    context = {
        'quiz': quiz,
        'total_questions': quiz.total_questions,
        'total_marks': quiz.total_marks,
        'past_attempts': past_attempts,
        'best_attempt': best_attempt,
    }
    return render(request, 'user/quiz_detail.html', context)


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    questions = quiz.questions.all()

    if not questions.exists():
        messages.warning(request, "This quiz currently does not have any questions. Please try another quiz.")
        return redirect('quiz_list')

    context = {
        'quiz': quiz,
        'questions': questions,
        'duration_seconds': quiz.duration_minutes * 60,
    }
    return render(request, 'user/take_quiz.html', context)


@login_required
def submit_quiz(request, quiz_id):
    if request.method != 'POST':
        return redirect('quiz_detail', quiz_id=quiz_id)

    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    questions = quiz.questions.all()

    if not questions.exists():
        messages.error(request, "Invalid quiz submission.")
        return redirect('quiz_list')

    total_marks_possible = 0
    total_score_obtained = 0
    correct_count = 0
    incorrect_count = 0
    unanswered_count = 0
    time_taken = int(request.POST.get('time_taken_seconds', 0))

    # Create the attempt object first
    attempt = QuizAttempt(
        user=request.user,
        quiz=quiz,
        time_taken_seconds=time_taken
    )

    user_answers = []

    for question in questions:
        total_marks_possible += question.marks
        field_name = f"question_{question.id}"
        selected_option = request.POST.get(field_name, '').strip()

        if not selected_option:
            unanswered_count += 1
            is_correct = False
            marks_obtained = 0
            selected_option = None
        elif selected_option == question.correct_option:
            correct_count += 1
            is_correct = True
            marks_obtained = question.marks
            total_score_obtained += marks_obtained
        else:
            incorrect_count += 1
            is_correct = False
            marks_obtained = 0

        user_answers.append(UserAnswer(
            attempt=attempt,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
            marks_obtained=marks_obtained
        ))

    # Calculate percentage and pass status
    percentage = (total_score_obtained / total_marks_possible * 100) if total_marks_possible > 0 else 0
    passed = percentage >= quiz.pass_percentage

    attempt.score = total_score_obtained
    attempt.total_score = total_marks_possible
    attempt.percentage = round(percentage, 2)
    attempt.passed = passed
    attempt.correct_count = correct_count
    attempt.incorrect_count = incorrect_count
    attempt.unanswered_count = unanswered_count
    attempt.save()

    # Save user answers with attempt reference
    for ua in user_answers:
        ua.attempt = attempt
    UserAnswer.objects.bulk_create(user_answers)

    messages.success(request, f"Quiz '{quiz.title}' submitted successfully!")
    return redirect('result_detail', attempt_id=attempt.id)


@login_required
def result_detail(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt.objects.select_related('quiz', 'quiz__subject', 'user'), id=attempt_id)
    
    # Only allow owner of attempt or admin
    if attempt.user != request.user and not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You do not have permission to view this result.")
        return redirect('user_dashboard')

    answers = attempt.answers.select_related('question').all()

    context = {
        'attempt': attempt,
        'answers': answers,
    }
    return render(request, 'user/result_detail.html', context)


@login_required
def quiz_history(request):
    attempts = QuizAttempt.objects.filter(user=request.user).select_related('quiz', 'quiz__subject').order_by('-completed_at')
    
    context = {
        'attempts': attempts,
    }
    return render(request, 'user/history.html', context)

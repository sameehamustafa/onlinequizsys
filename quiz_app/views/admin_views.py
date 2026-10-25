from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Avg, Q
from quiz_app.models import Subject, Quiz, Question, QuizAttempt
from quiz_app.forms import SubjectForm, QuizForm, QuestionForm
from quiz_app.decorators import admin_required


@admin_required
def admin_dashboard(request):
    total_subjects = Subject.objects.count()
    total_quizzes = Quiz.objects.count()
    total_questions = Question.objects.count()
    total_users = User.objects.filter(is_staff=False, is_superuser=False).count()
    total_attempts = QuizAttempt.objects.count()
    
    passed_attempts = QuizAttempt.objects.filter(passed=True).count()
    overall_pass_rate = round((passed_attempts / total_attempts * 100), 1) if total_attempts > 0 else 0
    avg_score = round(QuizAttempt.objects.aggregate(avg=Avg('percentage'))['avg'] or 0.0, 1)

    recent_attempts = QuizAttempt.objects.select_related('user', 'quiz', 'quiz__subject').order_by('-completed_at')[:8]
    recent_quizzes = Quiz.objects.select_related('subject').annotate(q_count=Count('questions')).order_by('-created_at')[:5]

    context = {
        'total_subjects': total_subjects,
        'total_quizzes': total_quizzes,
        'total_questions': total_questions,
        'total_users': total_users,
        'total_attempts': total_attempts,
        'overall_pass_rate': overall_pass_rate,
        'avg_score': avg_score,
        'recent_attempts': recent_attempts,
        'recent_quizzes': recent_quizzes,
    }
    return render(request, 'admin_panel/dashboard.html', context)


# --- SUBJECT MANAGEMENT ---
@admin_required
def subject_list(request):
    subjects = Subject.objects.annotate(
        quizzes_count=Count('quizzes'),
        questions_count=Count('quizzes__questions')
    ).order_by('name')
    return render(request, 'admin_panel/subject_list.html', {'subjects': subjects})


@admin_required
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save()
            messages.success(request, f"Subject '{subject.name}' created successfully!")
            return redirect('admin_subject_list')
        else:
            messages.error(request, "Error creating subject. Please check the form.")
    else:
        form = SubjectForm()
    return render(request, 'admin_panel/subject_form.html', {'form': form, 'action': 'Add'})


@admin_required
def subject_update(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, f"Subject '{subject.name}' updated successfully!")
            return redirect('admin_subject_list')
        else:
            messages.error(request, "Error updating subject. Please check the form.")
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'admin_panel/subject_form.html', {'form': form, 'subject': subject, 'action': 'Edit'})


@admin_required
def subject_delete(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        name = subject.name
        subject.delete()
        messages.success(request, f"Subject '{name}' and its associated quizzes were deleted.")
        return redirect('admin_subject_list')
    return render(request, 'admin_panel/subject_confirm_delete.html', {'subject': subject})


# --- QUIZ MANAGEMENT ---
@admin_required
def quiz_manage_list(request):
    subject_id = request.GET.get('subject')
    quizzes = Quiz.objects.select_related('subject').annotate(
        questions_count=Count('questions'),
        attempts_count=Count('attempts')
    ).order_by('-created_at')

    if subject_id:
        quizzes = quizzes.filter(subject_id=subject_id)

    subjects = Subject.objects.all()
    context = {
        'quizzes': quizzes,
        'subjects': subjects,
        'selected_subject': subject_id,
    }
    return render(request, 'admin_panel/quiz_list.html', context)


@admin_required
def quiz_create(request):
    initial_subject = request.GET.get('subject')
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            messages.success(request, f"Quiz '{quiz.title}' created successfully! You can now add questions.")
            return redirect('admin_question_list_by_quiz', quiz_id=quiz.id)
        else:
            messages.error(request, "Error creating quiz. Please check the form.")
    else:
        initial_data = {}
        if initial_subject:
            initial_data['subject'] = initial_subject
        form = QuizForm(initial=initial_data)
    return render(request, 'admin_panel/quiz_form.html', {'form': form, 'action': 'Add'})


@admin_required
def quiz_update(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, f"Quiz '{quiz.title}' updated successfully!")
            return redirect('admin_quiz_list')
        else:
            messages.error(request, "Error updating quiz. Please check the form.")
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'admin_panel/quiz_form.html', {'form': form, 'quiz': quiz, 'action': 'Edit'})


@admin_required
def quiz_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        title = quiz.title
        quiz.delete()
        messages.success(request, f"Quiz '{title}' and all associated questions/results were deleted.")
        return redirect('admin_quiz_list')
    return render(request, 'admin_panel/quiz_confirm_delete.html', {'quiz': quiz})


# --- QUESTION MANAGEMENT ---
@admin_required
def question_manage_list(request, quiz_id=None):
    quizzes = Quiz.objects.select_related('subject').all()
    questions = Question.objects.select_related('quiz', 'quiz__subject').order_by('quiz__title', 'id')
    selected_quiz = None

    if quiz_id:
        selected_quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = questions.filter(quiz=selected_quiz)
    else:
        filter_quiz = request.GET.get('quiz')
        if filter_quiz:
            questions = questions.filter(quiz_id=filter_quiz)
            selected_quiz = Quiz.objects.filter(id=filter_quiz).first()

    query = request.GET.get('q', '').strip()
    if query:
        questions = questions.filter(
            Q(question_text__icontains=query) |
            Q(option_a__icontains=query) |
            Q(option_b__icontains=query) |
            Q(option_c__icontains=query) |
            Q(option_d__icontains=query)
        )

    context = {
        'questions': questions,
        'quizzes': quizzes,
        'selected_quiz': selected_quiz,
        'query': query,
    }
    return render(request, 'admin_panel/question_list.html', context)


@admin_required
def question_create(request, quiz_id=None):
    initial_data = {}
    if quiz_id:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        initial_data['quiz'] = quiz

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            messages.success(request, "Question added successfully!")
            if 'save_and_add_another' in request.POST:
                return redirect('admin_question_create_for_quiz', quiz_id=question.quiz.id)
            return redirect('admin_question_list_by_quiz', quiz_id=question.quiz.id)
        else:
            messages.error(request, "Error adding question. Please check the fields.")
    else:
        form = QuestionForm(initial=initial_data)
    
    return render(request, 'admin_panel/question_form.html', {
        'form': form,
        'action': 'Add',
        'quiz_id': quiz_id
    })


@admin_required
def question_update(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question updated successfully!")
            return redirect('admin_question_list_by_quiz', quiz_id=question.quiz.id)
        else:
            messages.error(request, "Error updating question. Please check the fields.")
    else:
        form = QuestionForm(instance=question)
    return render(request, 'admin_panel/question_form.html', {
        'form': form,
        'question': question,
        'action': 'Edit',
        'quiz_id': question.quiz.id
    })


@admin_required
def question_delete(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    quiz_id = question.quiz.id
    if request.method == 'POST':
        question.delete()
        messages.success(request, "Question deleted successfully.")
        return redirect('admin_question_list_by_quiz', quiz_id=quiz_id)
    return render(request, 'admin_panel/question_confirm_delete.html', {'question': question})


# --- USER MANAGEMENT ---
@admin_required
def user_manage_list(request):
    users = User.objects.annotate(
        attempts_count=Count('quiz_attempts'),
        avg_score=Avg('quiz_attempts__percentage')
    ).order_by('-date_joined')
    
    query = request.GET.get('q', '').strip()
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    context = {
        'users': users,
        'query': query,
    }
    return render(request, 'admin_panel/user_list.html', context)


@admin_required
def user_history_view(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    attempts = QuizAttempt.objects.filter(user=target_user).select_related('quiz', 'quiz__subject').order_by('-completed_at')
    
    total_attempts = attempts.count()
    passed_attempts = attempts.filter(passed=True).count()
    avg_score = round(attempts.aggregate(avg=Avg('percentage'))['avg'] or 0.0, 1)

    context = {
        'target_user': target_user,
        'attempts': attempts,
        'total_attempts': total_attempts,
        'passed_attempts': passed_attempts,
        'avg_score': avg_score,
        'pass_rate': round((passed_attempts / total_attempts * 100), 1) if total_attempts > 0 else 0,
    }
    return render(request, 'admin_panel/user_history.html', context)


@admin_required
def user_delete(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        messages.error(request, "You cannot delete your own admin account.")
        return redirect('admin_user_list')

    if request.method == 'POST':
        username = target_user.username
        target_user.delete()
        messages.success(request, f"User account '{username}' has been deleted.")
        return redirect('admin_user_list')
    return render(request, 'admin_panel/user_confirm_delete.html', {'target_user': target_user})


# --- RESULTS & PERFORMANCE OVERVIEW ---
@admin_required
def results_overview(request):
    quiz_id = request.GET.get('quiz')
    user_id = request.GET.get('user')
    status = request.GET.get('status')

    attempts = QuizAttempt.objects.select_related('user', 'quiz', 'quiz__subject').order_by('-completed_at')

    if quiz_id:
        attempts = attempts.filter(quiz_id=quiz_id)
    if user_id:
        attempts = attempts.filter(user_id=user_id)
    if status == 'passed':
        attempts = attempts.filter(passed=True)
    elif status == 'failed':
        attempts = attempts.filter(passed=False)

    quizzes = Quiz.objects.all()
    users = User.objects.all()

    context = {
        'attempts': attempts,
        'quizzes': quizzes,
        'users': users,
        'selected_quiz': quiz_id,
        'selected_user': user_id,
        'selected_status': status,
    }
    return render(request, 'admin_panel/results_list.html', context)

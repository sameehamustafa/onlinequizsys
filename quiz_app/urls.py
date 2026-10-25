from django.urls import path
from quiz_app import views

urlpatterns = [
    # Auth URLs
    path('', views.login_view, name='root_login'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password_view, name='change_password'),

    # User Portal URLs
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('results/<int:attempt_id>/', views.result_detail, name='result_detail'),
    path('history/', views.quiz_history, name='quiz_history'),

    # Admin Management URLs
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    
    # Subject CRUD
    path('admin-panel/subjects/', views.subject_list, name='admin_subject_list'),
    path('admin-panel/subjects/add/', views.subject_create, name='admin_subject_create'),
    path('admin-panel/subjects/<int:subject_id>/edit/', views.subject_update, name='admin_subject_update'),
    path('admin-panel/subjects/<int:subject_id>/delete/', views.subject_delete, name='admin_subject_delete'),

    # Quiz CRUD
    path('admin-panel/quizzes/', views.quiz_manage_list, name='admin_quiz_list'),
    path('admin-panel/quizzes/add/', views.quiz_create, name='admin_quiz_create'),
    path('admin-panel/quizzes/<int:quiz_id>/edit/', views.quiz_update, name='admin_quiz_update'),
    path('admin-panel/quizzes/<int:quiz_id>/delete/', views.quiz_delete, name='admin_quiz_delete'),

    # Question CRUD
    path('admin-panel/questions/', views.question_manage_list, name='admin_question_list'),
    path('admin-panel/quizzes/<int:quiz_id>/questions/', views.question_manage_list, name='admin_question_list_by_quiz'),
    path('admin-panel/questions/add/', views.question_create, name='admin_question_create'),
    path('admin-panel/quizzes/<int:quiz_id>/questions/add/', views.question_create, name='admin_question_create_for_quiz'),
    path('admin-panel/questions/<int:question_id>/edit/', views.question_update, name='admin_question_update'),
    path('admin-panel/questions/<int:question_id>/delete/', views.question_delete, name='admin_question_delete'),

    # User Management
    path('admin-panel/users/', views.user_manage_list, name='admin_user_list'),
    path('admin-panel/users/<int:user_id>/history/', views.user_history_view, name='admin_user_history'),
    path('admin-panel/users/<int:user_id>/delete/', views.user_delete, name='admin_user_delete'),

    # Results Overview
    path('admin-panel/results/', views.results_overview, name='admin_results_list'),
]

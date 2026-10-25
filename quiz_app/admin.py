from django.contrib import admin
from .models import Subject, Quiz, Question, QuizAttempt, UserAnswer


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'quiz_count', 'created_at')
    search_fields = ('name', 'description')


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'duration_minutes', 'pass_percentage', 'is_published', 'created_at')
    list_filter = ('subject', 'is_published')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'question_text_short', 'correct_option', 'marks')
    list_filter = ('quiz__subject', 'quiz')
    search_fields = ('question_text',)

    def question_text_short(self, obj):
        return obj.question_text[:60] + '...' if len(obj.question_text) > 60 else obj.question_text
    question_text_short.short_description = "Question"


class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ('question', 'selected_option', 'is_correct', 'marks_obtained')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'total_score', 'percentage', 'passed', 'completed_at')
    list_filter = ('passed', 'quiz__subject', 'quiz')
    search_fields = ('user__username', 'quiz__title')
    inlines = [UserAnswerInline]

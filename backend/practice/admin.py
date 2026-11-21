from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    PracticeSession,
    StudyMaterial,
    PracticeQuestion,
    PracticeResponse
)


@admin.register(PracticeSession)
class PracticeSessionAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'course_name',
        'difficulty',
        'question_format',
        'mode',
        'status',
        'created_at',
    )
    list_filter = (
        'difficulty',
        'question_format',
        'mode',
        'status',
    )
    search_fields = (
        'student__full_name',
        'student__index_number',
        'course_name',
    )


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('session', 'file', 'uploaded_at')
    search_fields = ('session__course_name',)


@admin.register(PracticeQuestion)
class PracticeQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'session',
        'question_number',
        'question_type',
        'marks',
    )
    list_filter = ('question_type',)
    search_fields = ('question_text',)


@admin.register(PracticeResponse)
class PracticeResponseAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'question',
        'is_correct',
        'answered_at',
    )
    list_filter = ('is_correct',)
    search_fields = ('student__full_name',)
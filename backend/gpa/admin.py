from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SemesterResult


@admin.register(SemesterResult)
class SemesterResultAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'academic_year',
        'semester_name',
        'gpa',
        'credit_hours',
        'created_at',
    )

    list_filter = (
        'academic_year',
        'semester_name',
    )

    search_fields = (
        'student__full_name',
        'student__index_number',
    )

    ordering = ('student', 'academic_year')
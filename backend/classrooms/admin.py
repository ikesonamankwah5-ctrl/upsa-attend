from django.contrib import admin
from .models import Classroom


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'programme',
        'programme_type',
        'level',
        'academic_year',
        'created_by',
        'is_archived',
    )

    list_filter = (
        'programme',
        'programme_type',
        'level',
        'academic_year',
        'is_archived',
    )

    search_fields = (
        'name',
        'programme',
        'academic_year',
    )

    filter_horizontal = (
        'lecturers',
        'course_representatives',
    )
from django.contrib import admin
from .models import Semester, CourseOffering


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'academic_year',
        'start_date',
        'end_date',
        'is_active',
    )

    list_filter = (
        'academic_year',
        'is_active',
    )

    search_fields = (
        'name',
        'academic_year',
    )

    readonly_fields = (
        'created_at',
    )


@admin.register(CourseOffering)
class CourseOfferingAdmin(admin.ModelAdmin):

    list_display = (
        'course_code',
        'course_name',
        'semester',
        'classroom',
        'lecturer',
    )

    list_filter = (
        'semester',
        'classroom',
        'lecturer',
    )

    search_fields = (
        'course_code',
        'course_name',
        'lecturer__username',
    )
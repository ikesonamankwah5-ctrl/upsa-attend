from django.contrib import admin
from .models import (
    Semester,
    CourseOffering,
    PastQuestion,
    AnnualAcademicCalendar
)


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

    readonly_fields = ('created_at',)


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


@admin.register(PastQuestion)
class PastQuestionAdmin(admin.ModelAdmin):

    list_display = (
        'programme',
        'level',
        'course_name',
        'academic_year',
        'semester',
        'examination_title',
    )

    list_filter = (
        'programme',
        'level',
        'academic_year',
        'semester',
    )

    search_fields = (
        'programme',
        'course_name',
        'examination_title',
    )


@admin.register(AnnualAcademicCalendar)
class AnnualAcademicCalendarAdmin(admin.ModelAdmin):

    list_display = (
        'academic_year',
        'is_current',
        'uploaded_by',
        'uploaded_at',
    )

    list_filter = (
        'is_current',
        'academic_year',
    )

    search_fields = ('academic_year',)

    readonly_fields = (
        'uploaded_at',
        'uploaded_by',
    )

    def save_model(self, request, obj, form, change):

        if not obj.pk:
            obj.uploaded_by = request.user

        if obj.is_current:
            AnnualAcademicCalendar.objects.exclude(
                pk=obj.pk
            ).update(is_current=False)

        super().save_model(request, obj, form, change)
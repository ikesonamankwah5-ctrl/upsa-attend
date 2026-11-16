from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AttendanceSession, AttendanceRecord


class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = (
        'course_name',
        'course_code',
        'classroom',
        'lecture_date',
        'created_by'
    )

    list_filter = ('classroom', 'lecture_date')
    search_fields = ('course_name', 'course_code')

    inlines = [AttendanceRecordInline]


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'status')
    list_filter = ('status',)
    search_fields = ('student__full_name', 'student__index_number')
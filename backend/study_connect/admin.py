from django.contrib import admin
from .models import (
    StudyGroup,
    StudyGroupMembership,
    StudySession,
    GroupMessage,
)


class StudyGroupMembershipInline(admin.TabularInline):
    model = StudyGroupMembership
    extra = 0


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'course',
        'programme',
        'academic_level',
        'visibility',
        'created_by',
        'is_active',
    )

    list_filter = (
        'visibility',
        'programme',
        'academic_level',
        'is_active',
    )

    search_fields = (
        'title',
        'course',
        'programme',
        'created_by__username',
    )

    inlines = [StudyGroupMembershipInline]


@admin.register(StudyGroupMembership)
class StudyGroupMembershipAdmin(admin.ModelAdmin):

    list_display = (
        'group',
        'student',
        'role',
        'status',
        'joined_at',
    )

    list_filter = ('role', 'status')

    search_fields = (
        'group__title',
        'student__username',
    )


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'group',
        'session_type',
        'scheduled_at',
        'created_by',
    )

    list_filter = ('session_type',)

    search_fields = (
        'title',
        'group__title',
    )


@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):

    list_display = (
        'group',
        'sender',
        'created_at',
    )

    list_filter = ('created_at',)

    search_fields = (
        'group__title',
        'sender__username',
        'message',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )
from django.contrib import admin
from .models import StudySession, StudyMaterial, StudyChatMessage


class StudyMaterialInline(admin.TabularInline):
    model = StudyMaterial
    extra = 0
    readonly_fields = ['uploaded_at']


class StudyChatMessageInline(admin.TabularInline):
    model = StudyChatMessage
    extra = 0
    readonly_fields = ['created_at']


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):

    list_display = [
        'title',
        'user',
        'status',
        'created_at',
    ]

    list_filter = [
        'status',
        'created_at',
    ]

    search_fields = [
        'title',
        'user__username',
        'source_text',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
    ]

    inlines = [
        StudyMaterialInline,
        StudyChatMessageInline,
    ]


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):

    list_display = [
        'session',
        'file',
        'uploaded_at',
    ]

    list_filter = [
        'uploaded_at',
    ]

    search_fields = [
        'session__title',
        'session__user__username',
    ]

    readonly_fields = [
        'uploaded_at',
    ]


@admin.register(StudyChatMessage)
class StudyChatMessageAdmin(admin.ModelAdmin):

    list_display = [
        'session',
        'role',
        'created_at',
    ]

    list_filter = [
        'role',
        'created_at',
    ]

    search_fields = [
        'message',
        'session__title',
    ]
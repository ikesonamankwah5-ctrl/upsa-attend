from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'plan',
        'status',
        'start_date',
        'end_date',
        'is_admin_granted',
    )

    list_filter = (
        'plan',
        'status',
        'is_admin_granted',
    )

    search_fields = (
        'student__username',
        'student__email',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    ordering = ('-created_at',)
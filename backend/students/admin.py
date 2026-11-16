import csv
import secrets

from django.contrib import admin, messages
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'index_number',
        'classroom',
        'email',
        'phone_number',
    )

    search_fields = (
        'full_name',
        'index_number',
    )

    list_filter = (
        'classroom',
    )

    actions = [
        'generate_registration_codes',
    ]

    @admin.action(description='Generate registration codes for selected students')
    def generate_registration_codes(self, request, queryset):

        students = queryset.filter(
            user__isnull=True,
            registration_code_hash__isnull=True
        )

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = (
            'attachment; filename="student_registration_codes.csv"'
        )

        writer = csv.writer(response)

        writer.writerow([
            'Student Name',
            'Index Number',
            'Registration Code',
        ])

        generated_count = 0

        alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'

        for student in students:

            code = ''.join(
                secrets.choice(alphabet) for _ in range(8)
            )

            student.registration_code_hash = make_password(code)

            student.save(update_fields=['registration_code_hash'])

            writer.writerow([
                student.full_name,
                student.index_number,
                code,
            ])

            generated_count += 1

        if generated_count == 0:

            self.message_user(
                request,
                'No eligible students selected. They may already have accounts or registration codes.',
                level=messages.WARNING
            )

            return None

        return response
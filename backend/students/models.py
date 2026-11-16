from django.db import models
from django.conf import settings
from classrooms.models import Classroom


class Student(models.Model):

    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='students'
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_profile'
    )

    registration_code_hash = models.CharField(
        max_length=128,
        unique=True,
        null=True,
        blank=True
    )

    full_name = models.CharField(max_length=150)
    index_number = models.CharField(max_length=30, unique=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.index_number}"
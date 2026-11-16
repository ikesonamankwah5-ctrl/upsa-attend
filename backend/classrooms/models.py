import uuid

from django.db import models
from django.conf import settings


class Classroom(models.Model):

    name = models.CharField(max_length=100)
    programme = models.CharField(max_length=100)
    level = models.PositiveIntegerField()
    academic_year = models.CharField(max_length=20)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='classrooms'
    )

    lecturers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='assigned_classrooms'
    )

    course_representatives = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='representative_classrooms'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_archived = models.BooleanField(default=False)

    # Permanent, unique QR identity for each classroom.
    qr_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    def __str__(self):
        return self.name
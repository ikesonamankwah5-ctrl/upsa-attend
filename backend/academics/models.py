from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone


class Semester(models.Model):

    name = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=20)
    start_date = models.DateField()

    is_active = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_semesters'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def end_date(self):
        return self.start_date + timedelta(days=69)

    @property
    def has_ended(self):
        return timezone.localdate() > self.end_date

    @property
    def is_currently_active(self):
        return (
            self.is_active
            and self.start_date <= timezone.localdate() <= self.end_date
        )

    def __str__(self):
        return f"{self.name} - {self.academic_year}"


class CourseOffering(models.Model):

    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name='course_offerings'
    )

    classroom = models.ForeignKey(
        'classrooms.Classroom',
        on_delete=models.PROTECT,
        related_name='course_offerings'
    )

    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=150)

    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='course_offerings'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['semester', 'classroom', 'course_code'],
                name='unique_course_per_classroom_semester'
            )
        ]

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"
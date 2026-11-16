from django.db import models
from django.conf import settings

from classrooms.models import Classroom
from students.models import Student
from academics.models import CourseOffering


class AttendanceSession(models.Model):

    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='attendance_sessions'
    )

    course_offering = models.ForeignKey(
        CourseOffering,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='attendance_sessions'
    )

    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20)
    lecture_date = models.DateField()

    # Controls whether students can scan and check in.
    is_open = models.BooleanField(default=False)

    # Records when the lecturer opens attendance.
    opened_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_code} - {self.lecture_date}"


class AttendanceRecord(models.Model):

    PRESENT = 'Present'
    ABSENT = 'Absent'

    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
    ]

    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name='records'
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=ABSENT
    )

    # Records when the student checked in.
    checked_in_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'student'],
                name='unique_student_per_attendance_session'
            )
        ]

    def __str__(self):
        return f"{self.student.full_name} - {self.status}"
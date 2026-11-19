from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from students.models import Student


class SemesterResult(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='semester_results'
    )

    academic_year = models.CharField(max_length=20)

    semester_name = models.CharField(max_length=50)

    gpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(4)
        ]
    )

    credit_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['academic_year', 'semester_name']

        constraints = [
            models.UniqueConstraint(
                fields=['student', 'academic_year', 'semester_name'],
                name='unique_student_semester_result'
            )
        ]

    def __str__(self):
        return (
            f"{self.student.full_name} - "
            f"{self.semester_name} ({self.academic_year})"
        )

    @classmethod
    def calculate_cgpa(cls, student):

        results = cls.objects.filter(student=student)

        total_quality_points = sum(
            (
                result.gpa * result.credit_hours
                for result in results
            ),
            Decimal('0')
        )

        total_credit_hours = sum(
            (
                result.credit_hours
                for result in results
            ),
            Decimal('0')
        )

        if total_credit_hours == 0:
            return Decimal('0.00')

        return (
            total_quality_points / total_credit_hours
        ).quantize(Decimal('0.01'))
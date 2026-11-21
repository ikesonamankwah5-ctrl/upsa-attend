from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator
)
from students.models import Student


class PracticeSession(models.Model):

    DIFFICULTY_CHOICES = [
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
    ]

    QUESTION_FORMAT_CHOICES = [
        ('OBJECTIVE', 'Objective'),
        ('THEORY', 'Theory'),
        ('MIXED', 'Mixed'),
    ]

    MODE_CHOICES = [
        ('PRACTICE', 'Practice'),
        ('EXAMINATION', 'Examination'),
        ('REVISION', 'Revision'),
        ('CHALLENGE', 'Challenge'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='practice_sessions'
    )

    course_name = models.CharField(max_length=150)

    topic = models.CharField(
        max_length=200,
        blank=True
    )

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='MEDIUM'
    )

    question_format = models.CharField(
        max_length=15,
        choices=QUESTION_FORMAT_CHOICES,
        default='OBJECTIVE'
    )

    mode = models.CharField(
        max_length=15,
        choices=MODE_CHOICES,
        default='PRACTICE'
    )

    number_of_questions = models.PositiveIntegerField(
        default=20,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )

    time_limit_minutes = models.PositiveIntegerField(
        default=30,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(180)
        ]
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_name} - {self.student.full_name}"

    class Meta:
        ordering = ['-created_at']


class StudyMaterial(models.Model):

    session = models.ForeignKey(
        PracticeSession,
        on_delete=models.CASCADE,
        related_name='materials'
    )

    file = models.FileField(
        upload_to='practice/materials/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'ppt', 'pptx']
            )
        ]
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Material for {self.session.course_name}"


class PracticeQuestion(models.Model):

    QUESTION_TYPES = [
        ('OBJECTIVE', 'Objective'),
        ('THEORY', 'Theory'),
    ]

    session = models.ForeignKey(
        PracticeSession,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question_text = models.TextField()

    question_type = models.CharField(
        max_length=15,
        choices=QUESTION_TYPES
    )

    options = models.JSONField(
        default=list,
        blank=True
    )

    correct_answer = models.TextField(blank=True)

    explanation = models.TextField(blank=True)

    model_answer = models.TextField(blank=True)

    marks = models.PositiveIntegerField(default=1)

    question_number = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['question_number']

    def __str__(self):
        return f"Question {self.question_number} - {self.session.course_name}"


class PracticeResponse(models.Model):

    question = models.ForeignKey(
        PracticeQuestion,
        on_delete=models.CASCADE,
        related_name='responses'
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='practice_responses'
    )

    answer_text = models.TextField(blank=True)

    is_correct = models.BooleanField(
        null=True,
        blank=True
    )

    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'student'],
                name='unique_student_practice_response'
            )
        ]

    def __str__(self):
        return f"{self.student.full_name} - Question {self.question.question_number}"
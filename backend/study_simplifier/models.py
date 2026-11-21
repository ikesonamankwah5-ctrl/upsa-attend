from django.db import models
from django.conf import settings


class StudySession(models.Model):

    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'

    STATUS_CHOICES = [
        (PROCESSING, 'Processing'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='study_simplifier_sessions'
    )

    title = models.CharField(max_length=200)

    source_text = models.TextField(
        blank=True,
        help_text='Original study material provided by the student.'
    )

    uploaded_file = models.FileField(
        upload_to='study_simplifier/materials/',
        blank=True,
        null=True
    )

    simplified_explanation = models.TextField(blank=True)

    summary = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PROCESSING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.user}'


class StudyMaterial(models.Model):

    session = models.ForeignKey(
        StudySession,
        on_delete=models.CASCADE,
        related_name='study_materials'
    )

    file = models.FileField(
        upload_to='study_simplifier/materials/'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f'{self.file.name} - {self.session.title}'


class StudyChatMessage(models.Model):

    USER = 'USER'
    ASSISTANT = 'ASSISTANT'

    ROLE_CHOICES = [
        (USER, 'User'),
        (ASSISTANT, 'Assistant'),
    ]

    session = models.ForeignKey(
        StudySession,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.role} - {self.session.title}'
from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone


class StudyGroup(models.Model):

    VISIBILITY_CHOICES = [
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
    ]

    title = models.CharField(max_length=150)

    description = models.TextField()

    course = models.CharField(max_length=150)

    programme = models.CharField(max_length=150)

    academic_level = models.CharField(max_length=50)

    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='PUBLIC'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_study_groups'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def member_count(self):
        return self.memberships.filter(status='ACTIVE').count()


class StudyGroupMembership(models.Model):

    ROLE_CHOICES = [
        ('ADMIN', 'Group Administrator'),
        ('MEMBER', 'Member'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('PENDING', 'Pending Approval'),
    ]

    group = models.ForeignKey(
        StudyGroup,
        on_delete=models.CASCADE,
        related_name='memberships'
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='study_group_memberships'
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='MEMBER'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'student')

    def __str__(self):
        return f"{self.student} - {self.group}"


class StudySession(models.Model):

    SESSION_TYPES = [
        ('VIRTUAL', 'Virtual'),
        ('PHYSICAL', 'Physical'),
    ]

    group = models.ForeignKey(
        StudyGroup,
        on_delete=models.CASCADE,
        related_name='study_sessions'
    )

    title = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    session_type = models.CharField(
        max_length=10,
        choices=SESSION_TYPES,
        default='VIRTUAL'
    )

    meeting_location = models.CharField(
        max_length=255,
        blank=True
    )

    meeting_link = models.URLField(blank=True)

    scheduled_at = models.DateTimeField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organised_study_sessions'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.group.title}"

    @property
    def is_upcoming(self):
        return self.scheduled_at >= timezone.now()
class GroupMessage(models.Model):

    group = models.ForeignKey(
        StudyGroup,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='study_group_messages'
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender} - {self.group.title}"
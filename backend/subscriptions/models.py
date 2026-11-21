from django.db import models
from django.conf import settings
from django.utils import timezone


class Subscription(models.Model):

    PLAN_CHOICES = [
        ('FREE', 'Free'),
        ('WEEKLY', 'Weekly Premium'),
        ('MONTHLY', 'Monthly Premium'),
        ('SEMESTER', 'Semester Premium'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    plan = models.CharField(
        max_length=15,
        choices=PLAN_CHOICES,
        default='FREE'
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    start_date = models.DateTimeField(
        default=timezone.now
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True
    )

    is_admin_granted = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def is_premium(self):

        if self.plan == 'FREE':
            return False

        if self.status != 'ACTIVE':
            return False

        if self.end_date and timezone.now() >= self.end_date:
            return False

        return True

    def __str__(self):
        return f"{self.student} - {self.get_plan_display()}"


class Payment(models.Model):

    PLAN_CHOICES = [
        ('WEEKLY', 'Weekly Premium'),
        ('MONTHLY', 'Monthly Premium'),
        ('SEMESTER', 'Semester Premium'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Successful'),
        ('FAILED', 'Failed'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    plan = models.CharField(
        max_length=15,
        choices=PLAN_CHOICES
    )

    amount = models.PositiveIntegerField(
        help_text='Amount in pesewas'
    )

    currency = models.CharField(
        max_length=3,
        default='GHS'
    )

    reference = models.CharField(
        max_length=100,
        unique=True
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.student} - {self.reference} - {self.status}"
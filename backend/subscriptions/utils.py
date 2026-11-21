from django.utils import timezone
from .models import Subscription


def has_premium_access(user):

    if not user.is_authenticated:
        return False

    now = timezone.now()

    return Subscription.objects.filter(
        student=user,
        plan__in=['WEEKLY', 'MONTHLY', 'SEMESTER'],
        status='ACTIVE'
    ).filter(
        models_expiry_filter(now)
    ).exists()


def models_expiry_filter(now):
    from django.db.models import Q

    return Q(end_date__isnull=True) | Q(end_date__gt=now)
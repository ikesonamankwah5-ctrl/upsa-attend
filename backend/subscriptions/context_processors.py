from .utils import has_premium_access


def subscription_status(request):

    if not request.user.is_authenticated:
        return {
            'is_premium': False,
        }

    return {
        'is_premium': has_premium_access(request.user),
    }
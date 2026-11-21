from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .utils import has_premium_access


def premium_required(view_func):

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):

        if not has_premium_access(request.user):
            messages.warning(
                request,
                "This feature requires a Premium subscription. "
                "Please upgrade your account to continue."
            )

            return redirect('dashboard')

        return view_func(request, *args, **kwargs)

    return wrapper
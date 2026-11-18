import re

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db import transaction, IntegrityError

from students.models import Student


# --------------------------------------------------
# STUDENT REGISTRATION
# --------------------------------------------------

def register(request):

    if request.method == 'POST':

        index_number = request.POST.get('index_number', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([index_number, phone_number, username, password, confirm_password]):
            messages.error(request, 'Please complete all fields.')
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken.')
            return redirect('register')

        try:
            student = Student.objects.get(index_number=index_number)
        except Student.DoesNotExist:
            messages.error(
                request,
                'This index number is not registered in UPSA Attend.'
            )
            return redirect('register')

        if student.user is not None:
            messages.error(
                request,
                'An account already exists for this student. Please log in.'
            )
            return redirect('login')

        user = User(
            username=username,
            first_name=student.full_name,
            email=f'{student.index_number}@upsamail.edu.gh'
        )

        try:
            validate_password(password, user=user)
        except ValidationError as error:
            for message in error.messages:
                messages.error(request, message)
            return redirect('register')

        try:
            with transaction.atomic():

                student = Student.objects.select_for_update().get(
                    index_number=index_number
                )

                if student.user is not None:
                    messages.error(
                        request,
                        'An account already exists for this student. Please log in.'
                    )
                    return redirect('login')

                user.set_password(password)
                user.save()

                student.user = user
                student.phone_number = phone_number
                student.save(update_fields=['user', 'phone_number'])

            messages.success(
                request,
                'Registration successful. You can now log in.'
            )

            return redirect('login')

        except IntegrityError:
            messages.error(
                request,
                'Registration could not be completed. Please try again.'
            )
            return redirect('register')

    return render(request, 'accounts/register.html')


# --------------------------------------------------
# USER LOGIN
# --------------------------------------------------

def user_login(request):

    next_url = request.POST.get('next') or request.GET.get('next', '')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure()
            ):
                return redirect(next_url)

            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'accounts/login.html',
        {'next': next_url}
    )


# --------------------------------------------------
# USER DASHBOARD
# --------------------------------------------------

@login_required
def dashboard(request):

    return render(
        request,
        'accounts/dashboard.html'
    )


# --------------------------------------------------
# USER LOGOUT
# --------------------------------------------------

@require_POST
def user_logout(request):

    logout(request)

    messages.success(
        request,
        'You have successfully logged out.'
    )

    return redirect('login')
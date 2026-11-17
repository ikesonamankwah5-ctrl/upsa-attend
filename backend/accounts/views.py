import re

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db import transaction, IntegrityError

from students.models import Student


# STUDENT REGISTRATION
def register(request):

    if request.method == 'POST':

        index_number = request.POST.get(
            'index_number', ''
        ).strip()

        phone_number = request.POST.get(
            'phone_number', ''
        ).strip()

        username = request.POST.get(
            'username', ''
        ).strip()

        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([
            index_number,
            phone_number,
            username,
            password,
            confirm_password
        ]):
            messages.error(
                request,
                'Please complete all required fields.'
            )
            return redirect('register')

        # Check the imported student database.
        student = Student.objects.filter(
            index_number=index_number
        ).first()

        if not student:
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

        # Validate phone number.
        cleaned_phone = re.sub(r'[\s-]', '', phone_number)

        if not re.fullmatch(r'\+?\d{9,15}', cleaned_phone):
            messages.error(
                request,
                'Please enter a valid phone number.'
            )
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                'This username is already taken.'
            )
            return redirect('register')

        if password != confirm_password:
            messages.error(
                request,
                'Passwords do not match.'
            )
            return redirect('register')

        user = User(
            username=username,
            first_name=student.full_name
        )

        try:
            validate_password(password, user=user)

        except ValidationError as errors:
            for error in errors:
                messages.error(request, error)

            return redirect('register')

        try:
            with transaction.atomic():

                # Lock the student record to prevent duplicate registration.
                student = Student.objects.select_for_update().get(
                    index_number=index_number
                )

                if student.user is not None:
                    messages.error(
                        request,
                        'This student has already registered.'
                    )
                    return redirect('login')

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=student.full_name,
                    email=student.email or ''
                )

                student.user = user
                student.phone_number = cleaned_phone

                student.save(
                    update_fields=['user', 'phone_number']
                )

        except IntegrityError:
            messages.error(
                request,
                'Registration could not be completed. Please check your details.'
            )
            return redirect('register')

        messages.success(
            request,
            'Your UPSA Attend account has been created successfully. Please log in.'
        )

        return redirect('login')

    return render(request, 'accounts/register.html')


# LOGIN
def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


# DASHBOARD
@login_required
def dashboard(request):

    return render(request, 'accounts/dashboard.html')


# LOGOUT
@login_required
@require_POST
def user_logout(request):

    logout(request)

    return redirect('login')
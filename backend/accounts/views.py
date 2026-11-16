import secrets
import time

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib import messages
from django.db import transaction

from students.models import Student


# STUDENT REGISTRATION - REQUEST OTP
def register(request):

    if request.method == 'POST':

        index_number = request.POST.get(
            'index_number', ''
        ).strip()

        if not index_number:
            messages.error(request, 'Please enter your index number.')
            return redirect('register')

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

        email = f'{student.index_number}@upsamail.edu.gh'

        # Prevent overriding an existing, different student email.
        if student.email and student.email.strip().lower() != email.lower():
            messages.error(
                request,
                'Your registered email requires administrator verification.'
            )
            return redirect('register')

        # Prevent repeated OTP requests within 60 seconds.
        last_request = request.session.get('otp_last_request', 0)

        if time.time() - last_request < 60:
            messages.error(
                request,
                'Please wait one minute before requesting another code.'
            )
            return redirect('register')

        otp = str(secrets.randbelow(900000) + 100000)

        try:
            send_mail(
                subject='UPSA Attend Email Verification',
                message=(
                    f'Hello {student.full_name},\n\n'
                    f'Your UPSA Attend verification code is: {otp}\n\n'
                    'This code expires in 10 minutes.\n'
                    'If you did not request this code, please ignore this email.'
                ),
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )

        except Exception:
            messages.error(
                request,
                'Unable to send the verification email. Please try again later.'
            )
            return redirect('register')

        request.session['registration_student_id'] = student.id
        request.session['registration_otp_hash'] = make_password(otp)
        request.session['registration_otp_expiry'] = time.time() + 600
        request.session['registration_otp_attempts'] = 0
        request.session['otp_last_request'] = time.time()

        return redirect('verify_email')

    return render(request, 'accounts/register.html')


# VERIFY OTP AND CREATE STUDENT ACCOUNT
def verify_email(request):

    student_id = request.session.get('registration_student_id')
    otp_hash = request.session.get('registration_otp_hash')
    expiry = request.session.get('registration_otp_expiry')

    if not student_id or not otp_hash or not expiry:
        messages.error(
            request,
            'Please begin registration again.'
        )
        return redirect('register')

    if time.time() > expiry:
        request.session.pop('registration_student_id', None)
        request.session.pop('registration_otp_hash', None)
        request.session.pop('registration_otp_expiry', None)
        request.session.pop('registration_otp_attempts', None)

        messages.error(
            request,
            'Your verification code has expired. Please register again.'
        )
        return redirect('register')

    student = Student.objects.filter(id=student_id).first()

    if not student or student.user is not None:
        messages.error(
            request,
            'This student record is unavailable for registration.'
        )
        return redirect('register')

    if request.method == 'POST':

        otp = request.POST.get('otp', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        attempts = request.session.get(
            'registration_otp_attempts', 0
        )

        if attempts >= 5:
            request.session.pop('registration_student_id', None)
            request.session.pop('registration_otp_hash', None)
            request.session.pop('registration_otp_expiry', None)
            request.session.pop('registration_otp_attempts', None)

            messages.error(
                request,
                'Too many incorrect attempts. Please start registration again.'
            )
            return redirect('register')

        if not check_password(otp, otp_hash):

            request.session['registration_otp_attempts'] = attempts + 1

            messages.error(
                request,
                'Incorrect verification code.'
            )
            return redirect('verify_email')

        if not username or not password:
            messages.error(
                request,
                'Please complete all required fields.'
            )
            return redirect('verify_email')

        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                'This username is already taken.'
            )
            return redirect('verify_email')

        if password != confirm_password:
            messages.error(
                request,
                'Passwords do not match.'
            )
            return redirect('verify_email')

        email = f'{student.index_number}@upsamail.edu.gh'

        user = User(
            username=username,
            first_name=student.full_name,
            email=email
        )

        try:
            validate_password(password, user=user)
        except ValidationError as errors:
            for error in errors:
                messages.error(request, error)
            return redirect('verify_email')

        with transaction.atomic():

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=student.full_name
            )

            student.user = user
            student.email = email
            student.save(update_fields=['user', 'email'])

        request.session.pop('registration_student_id', None)
        request.session.pop('registration_otp_hash', None)
        request.session.pop('registration_otp_expiry', None)
        request.session.pop('registration_otp_attempts', None)

        messages.success(
            request,
            'Your UPSA Attend account has been created successfully. Please log in.'
        )

        return redirect('login')

    return render(request, 'accounts/verify_email.html', {
        'student': student,
        'email': f'{student.index_number}@upsamail.edu.gh'
    })


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
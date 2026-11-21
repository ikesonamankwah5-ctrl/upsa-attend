import hashlib
import hmac
import json
import uuid

import requests

from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Subscription, Payment
from .utils import has_premium_access


PREMIUM_FEATURES = {
    'question-generation': {
        'title': 'AI Question Generation',
        'description': 'Generate intelligent practice questions from your lecture notes.',
        'icon': '✧',
    },
    'ai-explanations': {
        'title': 'AI Explanations',
        'description': 'Understand why answers are correct with detailed AI explanations.',
        'icon': '💡',
    },
    'model-answers': {
        'title': 'AI Model Answers',
        'description': 'Access structured model answers for theory questions.',
        'icon': '📖',
    },
    'advanced-analytics': {
        'title': 'Advanced Analytics',
        'description': 'Identify weak areas and monitor your academic performance.',
        'icon': '📈',
    },
}


PLAN_DETAILS = {
    'WEEKLY': {
        'amount': 500,
        'duration': 7,
    },
    'MONTHLY': {
        'amount': 2000,
        'duration': 30,
    },
    'SEMESTER': {
        'amount': 5000,
        'duration': 120,
    },
}


# --------------------------------------------------
# PREMIUM FEATURE ACCESS
# --------------------------------------------------

@login_required
def premium_feature(request, feature):

    selected_feature = PREMIUM_FEATURES.get(feature)

    if not selected_feature:
        raise Http404('Premium feature not found.')

    context = {
        'feature': selected_feature,
        'is_premium': has_premium_access(request.user),
    }

    return render(
        request,
        'subscriptions/premium_feature.html',
        context
    )


# --------------------------------------------------
# PREMIUM PLANS
# --------------------------------------------------

@login_required
def premium_plans(request):

    context = {
        'is_premium': has_premium_access(request.user),
    }

    return render(
        request,
        'subscriptions/premium_plans.html',
        context
    )


# --------------------------------------------------
# INITIALIZE PAYSTACK PAYMENT
# --------------------------------------------------

@login_required
@require_POST
def initialize_payment(request):

    selected_plan = request.POST.get('plan', '').upper()

    if selected_plan not in PLAN_DETAILS:
        messages.error(request, 'Invalid subscription plan.')
        return redirect('subscriptions:plans')

    if has_premium_access(request.user):
        messages.info(
            request,
            'You already have an active Premium subscription.'
        )
        return redirect('subscriptions:plans')

    if not settings.PAYSTACK_SECRET_KEY:
        messages.error(
            request,
            'Payment service is currently unavailable.'
        )
        return redirect('subscriptions:plans')

    email = request.user.email

    student_profile = getattr(
        request.user,
        'student_profile',
        None
    )

    if student_profile and student_profile.email:
        email = student_profile.email.strip()

    if not email:
        messages.error(
            request,
            'Please provide an email address before making payment.'
        )
        return redirect('subscriptions:plans')

    plan = PLAN_DETAILS[selected_plan]

    reference = f'UPSAATTEND-{uuid.uuid4().hex.upper()}'

    payment = Payment.objects.create(
        student=request.user,
        plan=selected_plan,
        amount=plan['amount'],
        currency='GHS',
        reference=reference,
        status='PENDING'
    )

    callback_url = request.build_absolute_uri(
        reverse('subscriptions:verify_payment')
    )

    payload = {
        'email': email,
        'amount': plan['amount'],
        'currency': 'GHS',
        'reference': reference,
        'callback_url': callback_url,
        'metadata': {
            'payment_id': payment.id,
            'student_id': request.user.id,
            'plan': selected_plan,
        }
    }

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(
            f'{settings.PAYSTACK_BASE_URL}/transaction/initialize',
            json=payload,
            headers=headers,
            timeout=30
        )

        data = response.json()

        if (
            response.status_code == 200
            and data.get('status')
            and data.get('data', {}).get('authorization_url')
        ):
            return redirect(
                data['data']['authorization_url']
            )

        print(
            'PAYSTACK INITIALIZATION RESPONSE:',
            response.status_code,
            data
        )

        payment.status = 'FAILED'
        payment.save(update_fields=['status', 'updated_at'])

        messages.error(
            request,
            'Unable to initialize payment. Please try again.'
        )

    except (requests.RequestException, ValueError) as e:

        print(
            f"PAYSTACK INITIALIZATION ERROR: "
            f"{type(e).__name__}: {e}"
        )

        payment.status = 'FAILED'
        payment.save(update_fields=['status', 'updated_at'])

        messages.error(
            request,
            'Payment service could not be reached. Please try again.'
        )

    return redirect('subscriptions:plans')


# --------------------------------------------------
# VERIFY AND ACTIVATE PAYMENT
# --------------------------------------------------

def verify_and_activate_payment(reference):

    if not settings.PAYSTACK_SECRET_KEY:
        return 'retry'

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }

    try:
        response = requests.get(
            f'{settings.PAYSTACK_BASE_URL}/transaction/verify/{reference}',
            headers=headers,
            timeout=30
        )

        result = response.json()

    except (requests.RequestException, ValueError):
        return 'retry'

    if response.status_code != 200 or not result.get('status'):
        return 'retry'

    transaction_data = result.get('data', {})

    if transaction_data.get('status') != 'success':
        return 'failed'

    if transaction_data.get('reference') != reference:
        return 'invalid'

    with transaction.atomic():

        payment = Payment.objects.select_for_update().filter(
            reference=reference
        ).first()

        if not payment:
            return 'invalid'

        if payment.status == 'SUCCESS':
            return 'success'

        if payment.status != 'PENDING':
            return 'invalid'

        if transaction_data.get('amount') != payment.amount:
            return 'invalid'

        if transaction_data.get('currency') != payment.currency:
            return 'invalid'

        plan = PLAN_DETAILS.get(payment.plan)

        if not plan:
            return 'invalid'

        now = timezone.now()

        payment.status = 'SUCCESS'
        payment.paid_at = now

        payment.save(
            update_fields=[
                'status',
                'paid_at',
                'updated_at'
            ]
        )

        Subscription.objects.filter(
            student=payment.student,
            plan__in=['WEEKLY', 'MONTHLY', 'SEMESTER'],
            status='ACTIVE'
        ).update(
            status='EXPIRED'
        )

        Subscription.objects.create(
            student=payment.student,
            plan=payment.plan,
            status='ACTIVE',
            start_date=now,
            end_date=now + timedelta(days=plan['duration']),
            is_admin_granted=False
        )

    return 'success'


# --------------------------------------------------
# STUDENT PAYMENT CALLBACK
# --------------------------------------------------

@login_required
def verify_payment(request):

    reference = (
        request.GET.get('reference')
        or request.GET.get('trxref')
    )

    if not reference:
        messages.error(
            request,
            'Payment reference is missing.'
        )
        return redirect('subscriptions:plans')

    payment_exists = Payment.objects.filter(
        reference=reference,
        student=request.user
    ).exists()

    if not payment_exists:
        messages.error(
            request,
            'Payment record could not be found.'
        )
        return redirect('subscriptions:plans')

    result = verify_and_activate_payment(reference)

    if result == 'success':
        messages.success(
            request,
            'Payment successful! Your Premium subscription is now active.'
        )

    elif result == 'retry':
        messages.warning(
            request,
            'We could not verify your payment right now. Please try again.'
        )

    else:
        messages.error(
            request,
            'Payment could not be confirmed. No subscription was activated.'
        )

    return redirect('subscriptions:plans')


# --------------------------------------------------
# PAYSTACK WEBHOOK
# --------------------------------------------------

@csrf_exempt
@require_POST
def paystack_webhook(request):

    secret_key = settings.PAYSTACK_SECRET_KEY

    if not secret_key:
        return JsonResponse(
            {'message': 'Payment service unavailable.'},
            status=503
        )

    signature = request.headers.get('x-paystack-signature', '')

    expected_signature = hmac.new(
        secret_key.encode('utf-8'),
        request.body,
        hashlib.sha512
    ).hexdigest()

    if not hmac.compare_digest(
        signature,
        expected_signature
    ):
        return JsonResponse(
            {'message': 'Invalid signature.'},
            status=401
        )

    try:
        event = json.loads(request.body)

    except json.JSONDecodeError:
        return JsonResponse(
            {'message': 'Invalid request body.'},
            status=400
        )

    if event.get('event') != 'charge.success':
        return JsonResponse(
            {'message': 'Event ignored.'},
            status=200
        )

    reference = event.get('data', {}).get('reference')

    if not reference:
        return JsonResponse(
            {'message': 'Missing payment reference.'},
            status=400
        )

    result = verify_and_activate_payment(reference)

    if result == 'retry':
        return JsonResponse(
            {'message': 'Verification temporarily unavailable.'},
            status=500
        )

    if result == 'invalid':
        return JsonResponse(
            {'message': 'Payment could not be validated.'},
            status=400
        )

    return JsonResponse(
        {'message': 'Webhook processed successfully.'},
        status=200
    )
from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [

    path(
        'premium/<slug:feature>/',
        views.premium_feature,
        name='premium_feature'
    ),

    path(
        'plans/',
        views.premium_plans,
        name='plans'
    ),

    path(
        'payment/initialize/',
        views.initialize_payment,
        name='initialize_payment'
    ),

    path(
        'payment/verify/',
        views.verify_payment,
        name='verify_payment'
    ),

    path(
        'payment/webhook/',
        views.paystack_webhook,
        name='paystack_webhook'
    ),

]
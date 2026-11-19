from django.urls import path
from . import views

urlpatterns = [
    path('', views.cgpa_dashboard, name='cgpa_dashboard'),
]
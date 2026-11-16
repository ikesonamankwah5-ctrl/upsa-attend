from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_dashboard, name='report_dashboard'),

    path(
        'student-history/',
        views.student_attendance_history,
        name='student_attendance_history'
    ),

    path(
        'analytics/',
        views.attendance_analytics,
        name='attendance_analytics'
    ),

    path(
        'low-attendance/',
        views.low_attendance_alerts,
        name='low_attendance_alerts'
    ),
]
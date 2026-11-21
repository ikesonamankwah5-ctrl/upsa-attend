from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.attendance_list,
        name='attendance_list'
    ),

    path(
        'mark/<int:session_id>/',
        views.mark_attendance,
        name='mark_attendance'
    ),

    path(
        'session/<int:session_id>/toggle/',
        views.toggle_attendance_session,
        name='toggle_attendance_session'
    ),

    # Permanently delete an attendance session and its records
    path(
        'session/<int:session_id>/delete/',
        views.delete_attendance_session,
        name='delete_attendance_session'
    ),

    # Permanent classroom QR check-in
    path(
        'scan/<uuid:qr_token>/',
        views.qr_check_in,
        name='qr_check_in'
    ),

    # Rotating QR projector page
    path(
        'session/<int:session_id>/rotating-qr/',
        views.display_rotating_qr,
        name='display_rotating_qr'
    ),

    # Rotating QR image generator
    path(
        'session/<int:session_id>/rotating-qr-image/',
        views.rotating_qr_image,
        name='rotating_qr_image'
    ),

    # Student check-in using rotating QR
    path(
        'rotating-scan/<str:token>/',
        views.rotating_qr_check_in,
        name='rotating_qr_check_in'
    ),

    # Student camera scanner
    path(
        'scan-attendance/',
        views.scan_attendance,
        name='scan_attendance'
    ),

    # Student personal attendance history
    path(
        'my-attendance/',
        views.my_attendance,
        name='my_attendance'
    ),

]
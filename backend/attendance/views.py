from datetime import timedelta
from io import BytesIO

import qrcode

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core import signing
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.urls import reverse

from classrooms.models import Classroom
from students.models import Student
from academics.models import CourseOffering
from .models import AttendanceSession, AttendanceRecord
from .qr_security import generate_qr_token, verify_qr_token


LECTURE_DURATION = timedelta(hours=3)


# --------------------------------------------------
# USER ROLES
# --------------------------------------------------

def is_administrator(user):
    return (
        user.is_superuser
        or user.groups.filter(name="Administrator").exists()
    )


def is_lecturer(user):
    return user.groups.filter(name="Lecturer").exists()


def is_course_representative(user):
    return user.groups.filter(name="Course Representative").exists()


# --------------------------------------------------
# CLASSROOM ACCESS
# --------------------------------------------------

def get_managed_classrooms(user):

    if is_administrator(user):
        return Classroom.objects.all()

    if is_lecturer(user):
        return Classroom.objects.filter(lecturers=user)

    if is_course_representative(user):
        return Classroom.objects.filter(course_representatives=user)

    raise PermissionDenied


# --------------------------------------------------
# EXPIRE OLD ATTENDANCE SESSIONS
# --------------------------------------------------

def expire_old_sessions(sessions):

    now = timezone.now()

    for session in sessions:

        if (
            session.is_open
            and session.opened_at
            and now >= session.opened_at + LECTURE_DURATION
        ):
            session.is_open = False
            session.save(update_fields=['is_open'])


# --------------------------------------------------
# ATTENDANCE LIST AND SESSION CREATION
# --------------------------------------------------

@login_required
def attendance_list(request):

    administrator = is_administrator(request.user)
    lecturer = is_lecturer(request.user)
    representative = is_course_representative(request.user)

    if not administrator and not lecturer and not representative:
        raise PermissionDenied

    all_classrooms = get_managed_classrooms(request.user)

    classrooms = all_classrooms.filter(is_archived=False)

    if administrator:

        course_offerings = CourseOffering.objects.filter(
            semester__is_active=True,
            classroom__is_archived=False
        )

    elif lecturer:

        course_offerings = CourseOffering.objects.filter(
            lecturer=request.user,
            semester__is_active=True,
            classroom__lecturers=request.user,
            classroom__is_archived=False
        )

    else:

        course_offerings = CourseOffering.objects.filter(
            classroom__course_representatives=request.user,
            semester__is_active=True,
            classroom__is_archived=False
        )

    course_offerings = course_offerings.select_related(
        'semester',
        'classroom',
        'lecturer'
    )

    course_offerings = [
        offering for offering in course_offerings
        if offering.semester.is_currently_active
    ]

    if request.method == 'POST':

        offering_id = request.POST.get('course_offering')

        lecture_date = parse_date(
            request.POST.get('lecture_date', '')
        )

        offering = next(
            (
                item for item in course_offerings
                if str(item.id) == str(offering_id)
            ),
            None
        )

        if not offering:
            messages.error(
                request,
                'Please select a valid course assigned to your classroom.'
            )
            return redirect('attendance_list')

        if not lecture_date:
            messages.error(
                request,
                'Please provide a valid lecture date.'
            )
            return redirect('attendance_list')

        if not (
            offering.semester.start_date
            <= lecture_date
            <= offering.semester.end_date
        ):
            messages.error(
                request,
                'The lecture date must fall within the semester dates.'
            )
            return redirect('attendance_list')

        if offering.classroom.is_archived:
            messages.error(
                request,
                'This classroom is archived.'
            )
            return redirect('attendance_list')

        with transaction.atomic():

            session = AttendanceSession.objects.create(
                classroom=offering.classroom,
                course_offering=offering,
                course_name=offering.course_name,
                course_code=offering.course_code,
                lecture_date=lecture_date,
                created_by=request.user
            )

            students = Student.objects.filter(
                classroom=offering.classroom
            )

            AttendanceRecord.objects.bulk_create([
                AttendanceRecord(
                    session=session,
                    student=student,
                    status='Absent'
                )
                for student in students
            ])

        messages.success(
            request,
            'Attendance session created successfully. Open it when students are ready to check in.'
        )

        return redirect('attendance_list')

    sessions = AttendanceSession.objects.filter(
        classroom__in=all_classrooms
    ).select_related(
        'classroom',
        'course_offering__semester'
    ).order_by('-lecture_date')

    expire_old_sessions(sessions)

    return render(
        request,
        'attendance/attendance_list.html',
        {
            'classrooms': classrooms,
            'sessions': sessions,
            'course_offerings': course_offerings,
        }
    )


# --------------------------------------------------
# OPEN AND CLOSE ATTENDANCE
# --------------------------------------------------

@login_required
@require_POST
def toggle_attendance_session(request, session_id):

    if not (
        is_administrator(request.user)
        or is_lecturer(request.user)
        or is_course_representative(request.user)
    ):
        raise PermissionDenied

    managed_classrooms = get_managed_classrooms(request.user)

    session = get_object_or_404(
        AttendanceSession.objects.filter(
            classroom__in=managed_classrooms
        ),
        id=session_id
    )

    if session.classroom.is_archived:
        raise PermissionDenied(
            "Archived classroom sessions cannot be changed."
        )

    action = request.POST.get('action')

    if action == 'open':

        if not session.course_offering:
            messages.error(
                request,
                'This historical session has no course offering and cannot be opened for QR attendance.'
            )
            return redirect('attendance_list')

        semester = session.course_offering.semester

        if not semester.is_currently_active:
            messages.error(
                request,
                'This semester has ended or is not active.'
            )
            return redirect('attendance_list')

        if not (
            semester.start_date
            <= session.lecture_date
            <= semester.end_date
        ):
            messages.error(
                request,
                'The lecture date is outside the semester dates.'
            )
            return redirect('attendance_list')

        with transaction.atomic():

            AttendanceSession.objects.filter(
                classroom=session.classroom,
                is_open=True
            ).exclude(
                id=session.id
            ).update(
                is_open=False
            )

            session.is_open = True
            session.opened_at = timezone.now()

            session.save(
                update_fields=['is_open', 'opened_at']
            )

        messages.success(
            request,
            'Attendance opened successfully.'
        )

    elif action == 'close':

        session.is_open = False

        session.save(update_fields=['is_open'])

        messages.success(
            request,
            'Attendance session closed.'
        )

    else:

        messages.error(
            request,
            'Invalid session action.'
        )

    return redirect('attendance_list')


# --------------------------------------------------
# MANUAL ATTENDANCE
# --------------------------------------------------

@login_required
def mark_attendance(request, session_id):

    if not (
        is_administrator(request.user)
        or is_lecturer(request.user)
    ):
        raise PermissionDenied

    managed_classrooms = get_managed_classrooms(request.user)

    session = get_object_or_404(
        AttendanceSession.objects.filter(
            classroom__in=managed_classrooms
        ),
        id=session_id
    )

    if session.classroom.is_archived:
        raise PermissionDenied(
            "Attendance cannot be changed in an archived classroom."
        )

    if (
        session.course_offering
        and not session.course_offering.semester.is_currently_active
    ):
        raise PermissionDenied(
            "This semester has ended. Its attendance records are read-only."
        )

    records = session.records.select_related('student').all()

    if request.method == 'POST':

        with transaction.atomic():

            for record in records:

                status = request.POST.get(
                    f'attendance_{record.id}'
                )

                if status in ['Present', 'Absent']:

                    record.status = status

                    record.save(update_fields=['status'])

        messages.success(
            request,
            'Attendance saved successfully!'
        )

        return redirect('attendance_list')

    return render(
        request,
        'attendance/mark_attendance.html',
        {
            'session': session,
            'records': records
        }
    )


# --------------------------------------------------
# PERMANENT CLASSROOM QR CHECK-IN
# --------------------------------------------------

@login_required
def qr_check_in(request, qr_token):

    student = getattr(
        request.user,
        'student_profile',
        None
    )

    if student is None:
        messages.error(
            request,
            'Your account is not linked to a student record.'
        )
        return redirect('dashboard')

    classroom = get_object_or_404(
        Classroom,
        qr_token=qr_token,
        is_archived=False
    )

    if student.classroom_id != classroom.id:
        messages.error(
            request,
            'You are not registered in this classroom.'
        )
        return redirect('dashboard')

    open_sessions = list(
        AttendanceSession.objects.filter(
            classroom=classroom,
            is_open=True,
            course_offering__semester__is_active=True
        ).select_related(
            'course_offering__semester'
        )
    )

    expire_old_sessions(open_sessions)

    valid_sessions = [
        session for session in open_sessions
        if (
            session.is_open
            and session.opened_at
            and timezone.now() < session.opened_at + LECTURE_DURATION
            and session.course_offering.semester.is_currently_active
            and session.course_offering.semester.start_date
            <= session.lecture_date
            <= session.course_offering.semester.end_date
        )
    ]

    if not valid_sessions:
        messages.error(
            request,
            'There is no active attendance session for this classroom.'
        )
        return redirect('dashboard')

    if len(valid_sessions) > 1:
        messages.error(
            request,
            'More than one attendance session is open. Please contact your lecturer.'
        )
        return redirect('dashboard')

    session = valid_sessions[0]

    with transaction.atomic():

        record, created = AttendanceRecord.objects.select_for_update().get_or_create(
            session=session,
            student=student,
            defaults={'status': 'Absent'}
        )

        if record.status == 'Present':
            already_present = True

        else:
            record.status = 'Present'
            record.checked_in_at = timezone.now()

            record.save(
                update_fields=['status', 'checked_in_at']
            )

            already_present = False

    if already_present:
        messages.info(
            request,
            'Your attendance has already been recorded.'
        )

    else:
        messages.success(
            request,
            f'Attendance recorded successfully for {session.course_code}.'
        )

    return redirect('dashboard')


# --------------------------------------------------
# ROTATING QR PROJECTOR PAGE
# --------------------------------------------------

@login_required
def display_rotating_qr(request, session_id):

    if not (
        is_administrator(request.user)
        or is_lecturer(request.user)
        or is_course_representative(request.user)
    ):
        raise PermissionDenied

    session = get_object_or_404(
        AttendanceSession.objects.filter(
            classroom__in=get_managed_classrooms(request.user)
        ),
        id=session_id
    )

    if not session.is_open:
        messages.error(
            request,
            'This attendance session is not open.'
        )
        return redirect('attendance_list')

    if (
        not session.opened_at
        or timezone.now() >= session.opened_at + LECTURE_DURATION
    ):
        session.is_open = False
        session.save(update_fields=['is_open'])

        messages.error(
            request,
            'This attendance session has expired.'
        )
        return redirect('attendance_list')

    return render(
        request,
        'attendance/rotating_qr_display.html',
        {'session': session}
    )


# --------------------------------------------------
# ROTATING QR IMAGE GENERATOR
# --------------------------------------------------

@login_required
def rotating_qr_image(request, session_id):

    if not (
        is_administrator(request.user)
        or is_lecturer(request.user)
        or is_course_representative(request.user)
    ):
        raise PermissionDenied

    session = get_object_or_404(
        AttendanceSession.objects.filter(
            classroom__in=get_managed_classrooms(request.user)
        ),
        id=session_id
    )

    if (
        not session.is_open
        or not session.opened_at
        or timezone.now() >= session.opened_at + LECTURE_DURATION
    ):
        return HttpResponse(
            'Attendance session is closed or expired.',
            status=403
        )

    token = generate_qr_token(session.id)

    scan_path = reverse(
        'rotating_qr_check_in',
        kwargs={'token': token}
    )

    check_in_url = request.build_absolute_uri(scan_path)

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )

    qr.add_data(check_in_url)
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    image_buffer = BytesIO()

    image.save(
        image_buffer,
        format='PNG'
    )

    image_buffer.seek(0)

    response = HttpResponse(
        image_buffer.getvalue(),
        content_type='image/png'
    )

    response['Cache-Control'] = (
        'no-store, no-cache, must-revalidate, max-age=0'
    )

    return response


# --------------------------------------------------
# ROTATING QR STUDENT CHECK-IN
# --------------------------------------------------

@login_required
def rotating_qr_check_in(request, token):

    student = getattr(
        request.user,
        'student_profile',
        None
    )

    if student is None:
        messages.error(
            request,
            'Your account is not linked to a student record.'
        )
        return redirect('dashboard')

    # Decode and verify the signed QR token
    try:
        payload = signing.loads(
            token,
            salt="upsa-attend-rotating-qr-v1",
            max_age=60
        )

    except signing.SignatureExpired:
        messages.error(
            request,
            'This QR code has expired. Please scan the latest code.'
        )
        return redirect('dashboard')

    except signing.BadSignature:
        messages.error(
            request,
            'This QR code is invalid.'
        )
        return redirect('dashboard')

    session_id = payload.get('session_id')

    if not isinstance(session_id, int):
        messages.error(
            request,
            'Invalid attendance QR code.'
        )
        return redirect('dashboard')

    # Verify the 60-second QR time slot
    if not verify_qr_token(token, session_id):
        messages.error(
            request,
            'This QR code has expired. Please scan the latest code.'
        )
        return redirect('dashboard')

    session = get_object_or_404(
        AttendanceSession.objects.select_related(
            'classroom',
            'course_offering__semester'
        ),
        id=session_id
    )

    if not session.is_open or session.classroom.is_archived:
        messages.error(
            request,
            'This attendance session is closed.'
        )
        return redirect('dashboard')

    if student.classroom_id != session.classroom_id:
        messages.error(
            request,
            'You are not registered in this classroom.'
        )
        return redirect('dashboard')

    if (
        not session.opened_at
        or timezone.now() >= session.opened_at + LECTURE_DURATION
    ):
        messages.error(
            request,
            'The attendance period has ended.'
        )
        return redirect('dashboard')

    if (
        not session.course_offering
        or not session.course_offering.semester.is_currently_active
        or not (
            session.course_offering.semester.start_date
            <= session.lecture_date
            <= session.course_offering.semester.end_date
        )
    ):
        messages.error(
            request,
            'This attendance session is no longer valid.'
        )
        return redirect('dashboard')

    with transaction.atomic():

        record, created = AttendanceRecord.objects.select_for_update().get_or_create(
            session=session,
            student=student,
            defaults={'status': 'Absent'}
        )

        if record.status == 'Present':
            already_present = True

        else:
            record.status = 'Present'
            record.checked_in_at = timezone.now()

            record.save(
                update_fields=[
                    'status',
                    'checked_in_at'
                ]
            )

            already_present = False

    # Display the attendance confirmation page
    return render(
        request,
        'attendance/attendance_success.html',
        {
            'session': session,
            'record': record,
            'already_present': already_present,
        }
    )


# --------------------------------------------------
# STUDENT PERSONAL ATTENDANCE HISTORY
# --------------------------------------------------

@login_required
def my_attendance(request):

    student = getattr(request.user, 'student_profile', None)

    if student is None:
        messages.error(
            request,
            'Your account is not linked to a student record.'
        )
        return redirect('dashboard')

    records = AttendanceRecord.objects.filter(
        student=student
    ).select_related(
        'session',
        'session__classroom',
        'session__course_offering__semester'
    ).order_by('-session__lecture_date')

    total_classes = records.count()

    classes_attended = records.filter(
        status=AttendanceRecord.PRESENT
    ).count()

    classes_missed = records.filter(
        status=AttendanceRecord.ABSENT
    ).count()

    attendance_percentage = 0

    if total_classes > 0:
        attendance_percentage = round(
            (classes_attended / total_classes) * 100,
            2
        )

    return render(
        request,
        'attendance/my_attendance.html',
        {
            'student': student,
            'records': records,
            'total_classes': total_classes,
            'classes_attended': classes_attended,
            'classes_missed': classes_missed,
            'attendance_percentage': attendance_percentage,
        }
    )
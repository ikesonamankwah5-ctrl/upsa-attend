from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q

from classrooms.models import Classroom
from attendance.models import AttendanceSession, AttendanceRecord
from students.models import Student
from academics.models import CourseOffering, Semester


def is_administrator(user):
    return (
        user.is_superuser
        or user.groups.filter(name="Administrator").exists()
    )


def is_lecturer(user):
    return user.groups.filter(name="Lecturer").exists()


def get_user_classrooms(user):

    if is_administrator(user):
        return Classroom.objects.all()

    if is_lecturer(user):
        return Classroom.objects.filter(lecturers=user)

    raise PermissionDenied


@login_required
def report_dashboard(request):

    classrooms = get_user_classrooms(request.user)

    sessions = AttendanceSession.objects.filter(
        classroom__in=classrooms
    ).annotate(
        total_students=Count('records'),
        present_count=Count(
            'records',
            filter=Q(records__status='Present')
        ),
        absent_count=Count(
            'records',
            filter=Q(records__status='Absent')
        )
    ).order_by('-lecture_date')

    sessions = list(sessions)

    for session in sessions:
        if session.total_students > 0:
            session.attendance_percentage = round(
                (session.present_count / session.total_students) * 100, 1
            )
        else:
            session.attendance_percentage = 0

    return render(request, 'reports/report_dashboard.html', {
        'sessions': sessions
    })


@login_required
def student_attendance_history(request):

    classrooms = get_user_classrooms(request.user)

    search_query = request.GET.get('search', '')
    selected_student = None
    records = []

    students = Student.objects.filter(
        classroom__in=classrooms
    )

    if search_query:
        students = students.filter(
            Q(full_name__icontains=search_query) |
            Q(index_number__icontains=search_query)
        )

    student_id = request.GET.get('student_id')

    if student_id:
        selected_student = students.filter(id=student_id).first()

        if selected_student:
            records = list(
                AttendanceRecord.objects.filter(
                    student=selected_student,
                    session__classroom__in=classrooms
                ).select_related(
                    'session'
                ).order_by('-session__lecture_date')
            )

    total = len(records)
    present = sum(
        1 for record in records
        if record.status == 'Present'
    )
    absent = sum(
        1 for record in records
        if record.status == 'Absent'
    )

    percentage = round(
        (present / total) * 100, 1
    ) if total else 0

    return render(request, 'reports/student_history.html', {
        'students': students,
        'selected_student': selected_student,
        'records': records,
        'total': total,
        'present': present,
        'absent': absent,
        'percentage': percentage,
        'search_query': search_query,
    })


@login_required
def attendance_analytics(request):

    classrooms = get_user_classrooms(request.user)

    # Get course offerings accessible to the user.
    available_offerings = CourseOffering.objects.filter(
        classroom__in=classrooms
    ).select_related(
        'classroom',
        'semester',
        'lecturer'
    )

    # Restrict lecturers to their assigned courses.
    if is_lecturer(request.user) and not is_administrator(request.user):
        available_offerings = available_offerings.filter(
            lecturer=request.user
        )

    # Semester filter.
    selected_semester_id = request.GET.get('semester', '')

    # Course filter.
    selected_course_id = request.GET.get('course', '')

    # Apply filters to the course offerings.
    course_offerings = available_offerings

    if selected_semester_id:
        course_offerings = course_offerings.filter(
            semester_id=selected_semester_id
        )

    if selected_course_id:
        course_offerings = course_offerings.filter(
            id=selected_course_id
        )

    course_offerings = course_offerings.order_by(
        'course_code',
        'classroom_id'
    )

    student_data = []
    student_ids = set()
    total_lectures = 0

    # Calculate attendance separately for every course.
    for offering in course_offerings:

        lecture_count = AttendanceSession.objects.filter(
            classroom=offering.classroom,
            course_offering=offering
        ).count()

        total_lectures += lecture_count

        students = Student.objects.filter(
            classroom=offering.classroom
        ).annotate(
            present_lectures=Count(
                'attendance_records__session',
                filter=Q(
                    attendance_records__session__course_offering=offering,
                    attendance_records__status='Present'
                ),
                distinct=True
            )
        ).order_by('full_name')

        for student in students:

            present = student.present_lectures

            absent = max(
                lecture_count - present,
                0
            )

            percentage = round(
                (present / lecture_count) * 100,
                1
            ) if lecture_count else 0

            student_ids.add(student.id)

            student_data.append({
                'name': student.full_name,
                'index_number': student.index_number,
                'course_code': offering.course_code,
                'course_name': offering.course_name,
                'classroom': offering.classroom,
                'semester': offering.semester,
                'total': lecture_count,
                'present': present,
                'absent': absent,
                'percentage': percentage,
            })

    # Sort by course and then highest attendance percentage.
    student_data.sort(
        key=lambda item: (
            item['course_code'],
            -item['percentage']
        )
    )

    # Semester dropdown options.
    semesters = Semester.objects.filter(
        course_offerings__in=available_offerings
    ).distinct().order_by('-start_date')

    # Course dropdown options.
    courses = available_offerings

    if selected_semester_id:
        courses = courses.filter(
            semester_id=selected_semester_id
        )

    courses = courses.order_by('course_code')

    return render(request, 'reports/analytics.html', {
        'student_data': student_data,
        'total_lectures': total_lectures,
        'total_students': len(student_ids),
        'semesters': semesters,
        'courses': courses,
        'selected_semester_id': selected_semester_id,
        'selected_course_id': selected_course_id,
    })


@login_required
def low_attendance_alerts(request):

    classrooms = get_user_classrooms(request.user)

    students = Student.objects.filter(
        classroom__in=classrooms
    ).annotate(
        total_lectures=Count('attendance_records'),
        present_lectures=Count(
            'attendance_records',
            filter=Q(attendance_records__status='Present')
        )
    )

    low_attendance_students = []

    for student in students:

        if student.total_lectures == 0:
            continue

        percentage = round(
            (student.present_lectures / student.total_lectures) * 100,
            1
        )

        if percentage < 75:
            low_attendance_students.append({
                'name': student.full_name,
                'index_number': student.index_number,
                'total': student.total_lectures,
                'present': student.present_lectures,
                'absent': student.total_lectures - student.present_lectures,
                'percentage': percentage,
            })

    low_attendance_students.sort(
        key=lambda x: x['percentage']
    )

    return render(request, 'reports/low_attendance.html', {
        'low_attendance_students': low_attendance_students,
        'total_alerts': len(low_attendance_students),
    })
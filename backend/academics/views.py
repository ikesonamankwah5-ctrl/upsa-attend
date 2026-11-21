from pathlib import Path

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404

from .models import PastQuestion, AnnualAcademicCalendar


@login_required
def past_questions_library(request):

    # Only registered students can access the library.
    if not hasattr(request.user, 'student_profile'):
        messages.error(
            request,
            'The Past Questions Library is available to registered students only.'
        )
        return redirect('dashboard')

    past_questions = PastQuestion.objects.all().order_by(
        '-academic_year',
        'programme',
        'level',
        'course_name'
    )

    programmes = PastQuestion.objects.values_list(
        'programme', flat=True
    ).distinct().order_by('programme')

    levels = PastQuestion.objects.values_list(
        'level', flat=True
    ).distinct().order_by('level')

    courses = PastQuestion.objects.values_list(
        'course_name', flat=True
    ).distinct().order_by('course_name')

    academic_years = PastQuestion.objects.values_list(
        'academic_year', flat=True
    ).distinct().order_by('-academic_year')

    selected_programme = request.GET.get('programme', '')
    selected_level = request.GET.get('level', '')
    selected_course = request.GET.get('course', '')
    selected_year = request.GET.get('academic_year', '')
    selected_semester = request.GET.get('semester', '')

    if selected_programme:
        past_questions = past_questions.filter(
            programme=selected_programme
        )

    if selected_level:
        past_questions = past_questions.filter(
            level=selected_level
        )

    if selected_course:
        past_questions = past_questions.filter(
            course_name=selected_course
        )

    if selected_year:
        past_questions = past_questions.filter(
            academic_year=selected_year
        )

    if selected_semester:
        past_questions = past_questions.filter(
            semester=selected_semester
        )

    context = {
        'past_questions': past_questions,
        'programmes': programmes,
        'levels': levels,
        'courses': courses,
        'academic_years': academic_years,
        'selected_programme': selected_programme,
        'selected_level': selected_level,
        'selected_course': selected_course,
        'selected_year': selected_year,
        'selected_semester': selected_semester,
    }

    return render(
        request,
        'academics/past_questions_library.html',
        context
    )


@login_required
def view_past_question(request, question_id):

    # Only registered students can view past questions.
    if not hasattr(request.user, 'student_profile'):
        messages.error(
            request,
            'You are not authorised to view this question paper.'
        )
        return redirect('dashboard')

    question = get_object_or_404(
        PastQuestion,
        pk=question_id
    )

    if not question.question_paper:
        raise Http404('Question paper not found.')

    try:
        file_handle = question.question_paper.open('rb')
    except (FileNotFoundError, OSError, ValueError):
        raise Http404('The question paper could not be found.')

    response = FileResponse(
        file_handle,
        content_type='application/pdf'
    )

    filename = Path(question.question_paper.name).name

    response['Content-Disposition'] = (
        f'inline; filename="{filename}"'
    )

    response['X-Content-Type-Options'] = 'nosniff'

    return response


@login_required
def academic_calendar(request):

    calendars = AnnualAcademicCalendar.objects.all().order_by(
        '-is_current',
        '-uploaded_at'
    )

    return render(
        request,
        'academics/academic_calendar.html',
        {
            'calendars': calendars,
        }
    )
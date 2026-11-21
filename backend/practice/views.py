from datetime import timedelta
from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.views.decorators.http import require_POST

from students.models import Student

from .models import (
    PracticeSession,
    StudyMaterial,
    PracticeQuestion,
    PracticeResponse,
)

from .forms import PracticeSessionForm

from .services.document_extractor import extract_text_from_materials
from .services.question_generator import generate_practice_questions


ALLOWED_EXTENSIONS = {
    '.pdf',
    '.doc',
    '.docx',
    '.ppt',
    '.pptx',
}

MAX_FILE_SIZE = 10 * 1024 * 1024


# ==========================================
# PRACTICE DASHBOARD
# ==========================================

@login_required
def practice_dashboard(request):

    try:
        student = Student.objects.get(user=request.user)

    except Student.DoesNotExist:
        messages.error(
            request,
            'The Practice Centre is available to registered students only.'
        )
        return redirect('dashboard')

    sessions = PracticeSession.objects.filter(
        student=student
    ).order_by('-created_at')

    return render(
        request,
        'practice/practice_dashboard.html',
        {'sessions': sessions}
    )


# ==========================================
# CREATE PRACTICE SESSION
# ==========================================

@login_required
def create_practice_session(request):

    try:
        student = Student.objects.get(user=request.user)

    except Student.DoesNotExist:
        messages.error(
            request,
            'Only registered students can create practice sessions.'
        )
        return redirect('dashboard')

    if request.method == 'POST':

        form = PracticeSessionForm(request.POST)
        uploaded_files = request.FILES.getlist('materials')

        if not uploaded_files:
            form.add_error(
                None,
                'Please upload at least one lecture note.'
            )

        elif len(uploaded_files) > 10:
            form.add_error(
                None,
                'You can upload a maximum of 10 lecture notes per session.'
            )

        else:
            for uploaded_file in uploaded_files:

                extension = Path(uploaded_file.name).suffix.lower()

                if extension not in ALLOWED_EXTENSIONS:
                    form.add_error(
                        None,
                        f'{uploaded_file.name} is not an accepted file type.'
                    )
                    break

                if uploaded_file.size > MAX_FILE_SIZE:
                    form.add_error(
                        None,
                        f'{uploaded_file.name} exceeds the 10 MB file limit.'
                    )
                    break

                if uploaded_file.size == 0:
                    form.add_error(
                        None,
                        f'{uploaded_file.name} is empty.'
                    )
                    break

        if form.is_valid() and not form.errors:

            try:
                with transaction.atomic():

                    session = form.save(commit=False)
                    session.student = student
                    session.save()

                    for uploaded_file in uploaded_files:
                        StudyMaterial.objects.create(
                            session=session,
                            file=uploaded_file
                        )

                messages.success(
                    request,
                    'Your practice session and lecture notes have been saved successfully.'
                )

                return redirect('practice_dashboard')

            except (ValidationError, OSError):
                messages.error(
                    request,
                    'Something went wrong while saving your materials. Please try again.'
                )

    else:
        form = PracticeSessionForm()

    return render(
        request,
        'practice/create_practice_session.html',
        {'form': form}
    )


# ==========================================
# EXTRACT PRACTICE MATERIALS
# ==========================================

@login_required
@require_POST
def extract_practice_materials(request, session_id):

    try:
        student = Student.objects.get(user=request.user)

    except Student.DoesNotExist:
        messages.error(
            request,
            'Only registered students can access the Practice Centre.'
        )
        return redirect('dashboard')

    session = get_object_or_404(
        PracticeSession,
        id=session_id,
        student=student
    )

    materials = session.materials.all()

    if not materials.exists():
        messages.error(
            request,
            'No lecture notes were found for this session.'
        )
        return redirect('practice_dashboard')

    try:
        combined_text = extract_text_from_materials(materials)

        messages.success(
            request,
            f'Successfully extracted {len(combined_text):,} characters '
            f'from your {materials.count()} lecture note(s).'
        )

    except ValueError as error:
        messages.error(request, str(error))

    except Exception:
        messages.error(
            request,
            'An unexpected error occurred while reading your lecture notes.'
        )

    return redirect('practice_dashboard')


# ==========================================
# GENERATE PRACTICE QUESTIONS
# ==========================================

@login_required
@require_POST
def generate_session_questions(request, session_id):

    try:
        student = Student.objects.get(user=request.user)

    except Student.DoesNotExist:
        messages.error(
            request,
            'Only registered students can generate practice questions.'
        )
        return redirect('dashboard')

    session = get_object_or_404(
        PracticeSession,
        id=session_id,
        student=student
    )

    if session.questions.exists():
        messages.info(
            request,
            'Questions have already been generated for this session.'
        )
        return redirect('practice_dashboard')

    materials = session.materials.all()

    if not materials.exists():
        messages.error(
            request,
            'Please upload lecture notes before generating questions.'
        )
        return redirect('practice_dashboard')

    try:
        combined_text = extract_text_from_materials(materials)

        generated_questions = generate_practice_questions(
            source_text=combined_text,
            question_format=session.question_format,
            number_of_questions=session.number_of_questions
        )

        with transaction.atomic():

            for question in generated_questions:
                PracticeQuestion.objects.create(
                    session=session,
                    question_text=question['question_text'],
                    question_type=question['question_type'],
                    options=question['options'],
                    correct_answer=question['correct_answer'],
                    explanation=question['explanation'],
                    model_answer=question['model_answer'],
                    marks=question['marks'],
                    question_number=question['question_number'],
                )

            session.status = 'IN_PROGRESS'
            session.save(update_fields=['status'])

        messages.success(
            request,
            f'{len(generated_questions)} practice questions generated successfully!'
        )

    except ValueError as error:
        messages.error(request, str(error))

    except Exception:
        messages.error(
            request,
            'Something went wrong while generating questions. Please try again.'
        )

    return redirect('practice_dashboard')


# ==========================================
# EXAMINATION INTERFACE
# ==========================================

@login_required
def take_practice_session(request, session_id):

    try:
        student = Student.objects.get(user=request.user)

    except Student.DoesNotExist:
        messages.error(request, 'Registered students only.')
        return redirect('dashboard')

    session = get_object_or_404(
        PracticeSession,
        id=session_id,
        student=student
    )

    if session.status == 'COMPLETED':
        return redirect(
            'practice_results',
            session_id=session.id
        )

    questions = session.questions.all().order_by('question_number')

    if not questions.exists():
        messages.error(
            request,
            'No questions have been generated for this session.'
        )
        return redirect('practice_dashboard')

    if session.started_at is None:
        session.started_at = timezone.now()
        session.status = 'IN_PROGRESS'

        session.save(
            update_fields=['started_at', 'status']
        )

    deadline = session.started_at + timedelta(
        minutes=session.time_limit_minutes
    )

    remaining_seconds = max(
        0,
        int((deadline - timezone.now()).total_seconds())
    )

    if remaining_seconds <= 0:

        session.status = 'COMPLETED'
        session.submitted_at = timezone.now()

        session.save(
            update_fields=['status', 'submitted_at']
        )

        messages.warning(
            request,
            'Your examination time has expired.'
        )

        return redirect(
            'practice_results',
            session_id=session.id
        )

    saved_responses = {
        response.question_id: response.answer_text
        for response in PracticeResponse.objects.filter(
            student=student,
            question__session=session
        )
    }

    question_data = []

    for question in questions:

        question_data.append({
            'id': question.id,
            'number': question.question_number,
            'text': question.question_text,
            'type': question.question_type,
            'options': question.options,
            'marks': question.marks,
            'saved_answer': saved_responses.get(
                question.id,
                ''
            ),
        })

    context = {
        'session': session,
        'questions': question_data,
        'remaining_seconds': remaining_seconds,
    }

    return render(
        request,
        'practice/take_practice_session.html',
        context
    )


# ==========================================
# AUTOMATIC ANSWER SAVING
# ==========================================

@login_required
@require_POST
def save_practice_answer(request, session_id):

    try:
        student = Student.objects.get(user=request.user)

    except Student.DoesNotExist:
        return JsonResponse(
            {
                'success': False,
                'message': 'Registered students only.'
            },
            status=403
        )

    session = get_object_or_404(
        PracticeSession,
        id=session_id,
        student=student
    )

    if session.status == 'COMPLETED' or session.started_at is None:
        return JsonResponse(
            {
                'success': False,
                'message': 'This examination is no longer active.'
            },
            status=400
        )

    deadline = session.started_at + timedelta(
        minutes=session.time_limit_minutes
    )

    if timezone.now() >= deadline:
        return JsonResponse(
            {
                'success': False,
                'message': 'Examination time has expired.'
            },
            status=400
        )

    question_id = request.POST.get('question_id')
    answer = request.POST.get('answer', '').strip()

    if not question_id:
        return JsonResponse(
            {
                'success': False,
                'message': 'Question information is missing.'
            },
            status=400
        )

    question = get_object_or_404(
        PracticeQuestion,
        id=question_id,
        session=session
    )

    if question.question_type == 'OBJECTIVE':

        if answer and answer not in question.options:
            return JsonResponse(
                {
                    'success': False,
                    'message': 'Invalid answer option.'
                },
                status=400
            )

        is_correct = (
            answer == question.correct_answer
            if answer else False
        )

    else:
        is_correct = None

    PracticeResponse.objects.update_or_create(
        question=question,
        student=student,
        defaults={
            'answer_text': answer,
            'is_correct': is_correct,
        }
    )

    return JsonResponse({
        'success': True,
        'message': 'Answer saved.'
    })


# ==========================================
# SUBMIT EXAMINATION
# ==========================================

@login_required
@require_POST
def submit_practice_session(request, session_id):

    try:
        student = Student.objects.get(user=request.user)

    except Student.DoesNotExist:
        messages.error(request, 'Registered students only.')
        return redirect('dashboard')

    session = get_object_or_404(
        PracticeSession,
        id=session_id,
        student=student
    )

    if session.status == 'COMPLETED':
        return redirect(
            'practice_results',
            session_id=session.id
        )

    if session.started_at is None:
        messages.error(
            request,
            'Please start the examination first.'
        )
        return redirect('practice_dashboard')

    deadline = session.started_at + timedelta(
        minutes=session.time_limit_minutes
    )

    time_expired = timezone.now() >= deadline

    with transaction.atomic():

        # If the examination is still within time,
        # save all answers submitted with the form.
        if not time_expired:

            for question in session.questions.all():

                field_name = f'answer_{question.id}'

                answer = request.POST.get(
                    field_name,
                    ''
                ).strip()

                if question.question_type == 'OBJECTIVE':

                    if answer and answer not in question.options:
                        continue

                    is_correct = (
                        answer == question.correct_answer
                        if answer else False
                    )

                else:
                    is_correct = None

                PracticeResponse.objects.update_or_create(
                    question=question,
                    student=student,
                    defaults={
                        'answer_text': answer,
                        'is_correct': is_correct,
                    }
                )

        # If time has expired, preserve previously
        # autosaved answers instead of overwriting them.

        session.status = 'COMPLETED'
        session.submitted_at = timezone.now()

        session.save(
            update_fields=['status', 'submitted_at']
        )

    if time_expired:
        messages.warning(
            request,
            'Your examination time expired. Your previously saved answers have been preserved.'
        )
    else:
        messages.success(
            request,
            'Your examination has been submitted successfully.'
        )

    return redirect(
        'practice_results',
        session_id=session.id
    )


# ==========================================
# EXAMINATION RESULTS
# ==========================================

@login_required
def practice_results(request, session_id):

    try:
        student = Student.objects.get(user=request.user)

    except Student.DoesNotExist:
        messages.error(request, 'Registered students only.')
        return redirect('dashboard')

    session = get_object_or_404(
        PracticeSession,
        id=session_id,
        student=student,
        status='COMPLETED'
    )

    questions = session.questions.all().order_by(
        'question_number'
    )

    responses = {
        response.question_id: response
        for response in PracticeResponse.objects.filter(
            student=student,
            question__session=session
        )
    }

    total_objective_marks = 0
    earned_objective_marks = 0

    results = []

    for question in questions:

        response = responses.get(question.id)

        if question.question_type == 'OBJECTIVE':

            total_objective_marks += question.marks

            if response and response.is_correct:
                earned_objective_marks += question.marks

        results.append({
            'question': question,
            'response': response,
        })

    percentage = (
        round(
            earned_objective_marks / total_objective_marks * 100,
            2
        )
        if total_objective_marks else None
    )

    context = {
        'session': session,
        'results': results,
        'earned_objective_marks': earned_objective_marks,
        'total_objective_marks': total_objective_marks,
        'percentage': percentage,
    }

    return render(
        request,
        'practice/practice_results.html',
        context
    )
    # ==========================================
# DELETE INDIVIDUAL PRACTICE SESSION
# ==========================================

@login_required
@require_POST
def delete_practice_session(request, session_id):

    try:
        student = Student.objects.get(user=request.user)

    except Student.DoesNotExist:
        messages.error(request, 'Registered students only.')
        return redirect('dashboard')

    session = get_object_or_404(
        PracticeSession,
        id=session_id,
        student=student
    )

    files_to_delete = [
        (material.file.storage, material.file.name)
        for material in session.materials.all()
        if material.file
    ]

    with transaction.atomic():

        session.delete()

        transaction.on_commit(
            lambda: [
                storage.delete(name)
                for storage, name in files_to_delete
            ]
        )

    messages.success(
        request,
        'Practice session and its associated materials deleted successfully.'
    )

    return redirect('practice_dashboard')


# ==========================================
# CLEAR ALL PRACTICE HISTORY
# ==========================================

@login_required
@require_POST
def clear_practice_history(request):

    try:
        student = Student.objects.get(user=request.user)

    except Student.DoesNotExist:
        messages.error(request, 'Registered students only.')
        return redirect('dashboard')

    sessions = PracticeSession.objects.filter(
        student=student
    )

    files_to_delete = [
        (material.file.storage, material.file.name)
        for session in sessions
        for material in session.materials.all()
        if material.file
    ]

    with transaction.atomic():

        sessions.delete()

        transaction.on_commit(
            lambda: [
                storage.delete(name)
                for storage, name in files_to_delete
            ]
        )

    messages.success(
        request,
        'Your entire practice history has been cleared.'
    )

    return redirect('practice_dashboard')
from pathlib import Path

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.db import transaction

from .models import StudySession, StudyMaterial


@login_required
def dashboard(request):

    sessions = StudySession.objects.filter(
        user=request.user
    )

    context = {
        'sessions': sessions,
        'total_sessions': sessions.count(),
    }

    return render(
        request,
        'study_simplifier/dashboard.html',
        context
    )


@login_required
def create_session(request):

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        source_text = request.POST.get('source_text', '').strip()

        uploaded_files = request.FILES.getlist('uploaded_files')

        allowed_extensions = ['.pdf', '.docx', '.pptx', '.txt']

        if not title:
            messages.error(
                request,
                'Please provide a topic title.'
            )
            return redirect('study_simplifier:create_session')

        if not source_text and not uploaded_files:
            messages.error(
                request,
                'Please paste study material or upload at least one file.'
            )
            return redirect('study_simplifier:create_session')

        if len(uploaded_files) > 12:
            messages.error(
                request,
                'You can upload a maximum of 12 lecture notes per session.'
            )
            return redirect('study_simplifier:create_session')

        for uploaded_file in uploaded_files:

            file_extension = Path(uploaded_file.name).suffix.lower()

            if file_extension not in allowed_extensions:
                messages.error(
                    request,
                    f'{uploaded_file.name} has an unsupported format. '
                    'Upload PDF, DOCX, PPTX or TXT files.'
                )
                return redirect('study_simplifier:create_session')

            if uploaded_file.size > 20 * 1024 * 1024:
                messages.error(
                    request,
                    f'{uploaded_file.name} exceeds the 20MB file limit.'
                )
                return redirect('study_simplifier:create_session')

        with transaction.atomic():

            session = StudySession.objects.create(
                user=request.user,
                title=title,
                source_text=source_text
            )

            for uploaded_file in uploaded_files:

                StudyMaterial.objects.create(
                    session=session,
                    file=uploaded_file
                )

        messages.success(
            request,
            'Your study session and lecture notes have been saved successfully.'
        )

        return redirect(
            'study_simplifier:session_detail',
            session_id=session.id
        )

    return render(
        request,
        'study_simplifier/create_session.html'
    )


@login_required
def session_detail(request, session_id):

    session = get_object_or_404(
        StudySession,
        id=session_id,
        user=request.user
    )

    return render(
        request,
        'study_simplifier/session_detail.html',
        {
            'session': session,
            'messages': session.messages.all(),
        }
    )


@login_required
def download_material(request, session_id):

    session = get_object_or_404(
        StudySession,
        id=session_id,
        user=request.user
    )

    if not session.uploaded_file:
        raise Http404('No uploaded study material was found.')

    if not session.uploaded_file.storage.exists(
        session.uploaded_file.name
    ):
        raise Http404('The uploaded file could not be found.')

    return FileResponse(
        session.uploaded_file.open('rb'),
        as_attachment=True,
        filename=Path(session.uploaded_file.name).name
    )


@login_required
def download_study_material(request, session_id, material_id):

    session = get_object_or_404(
        StudySession,
        id=session_id,
        user=request.user
    )

    material = get_object_or_404(
        StudyMaterial,
        id=material_id,
        session=session
    )

    if not material.file.storage.exists(material.file.name):
        raise Http404('The uploaded file could not be found.')

    return FileResponse(
        material.file.open('rb'),
        as_attachment=True,
        filename=Path(material.file.name).name
    )
from io import BytesIO

import qrcode

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages

from .models import Classroom


def is_administrator(user):
    return (
        user.is_superuser
        or user.groups.filter(name="Administrator").exists()
    )


def is_lecturer(user):
    return user.groups.filter(name="Lecturer").exists()


@login_required
def classroom_list(request):

    administrator = is_administrator(request.user)
    lecturer = is_lecturer(request.user)

    if not administrator and not lecturer:
        raise PermissionDenied

    if request.method == 'POST':

        if not administrator:
            raise PermissionDenied

        action = request.POST.get('action')

        # CREATE CLASSROOM
        if action == 'create':

            Classroom.objects.create(
                name=request.POST.get('name'),
                programme=request.POST.get('programme'),
                level=request.POST.get('level'),
                academic_year=request.POST.get('academic_year'),
                created_by=request.user
            )

            messages.success(
                request,
                'Classroom created successfully!'
            )

        # ARCHIVE OR RESTORE CLASSROOM
        elif action in ['archive', 'restore']:

            classroom = get_object_or_404(
                Classroom,
                id=request.POST.get('classroom_id')
            )

            if action == 'archive':
                classroom.is_archived = True
                messages.success(
                    request,
                    'Classroom archived successfully!'
                )

            else:
                classroom.is_archived = False
                messages.success(
                    request,
                    'Classroom restored successfully!'
                )

            classroom.save()

        return redirect('classroom_list')

    # ACTIVE CLASSROOMS
    if administrator:

        classrooms = Classroom.objects.filter(
            is_archived=False
        )

        archived_classrooms = Classroom.objects.filter(
            is_archived=True
        )

    else:

        classrooms = Classroom.objects.filter(
            lecturers=request.user,
            is_archived=False
        )

        archived_classrooms = Classroom.objects.none()

    return render(request, 'classrooms/classroom_list.html', {
        'classrooms': classrooms,
        'archived_classrooms': archived_classrooms,
        'administrator': administrator,
    })


# GENERATE PERMANENT CLASSROOM QR CODE
@login_required
def classroom_qr_code(request, classroom_id):

    administrator = is_administrator(request.user)
    lecturer = is_lecturer(request.user)

    if not administrator and not lecturer:
        raise PermissionDenied

    if administrator:
        classrooms = Classroom.objects.all()
    else:
        classrooms = Classroom.objects.filter(
            lecturers=request.user
        )

    classroom = get_object_or_404(
        classrooms,
        id=classroom_id,
        is_archived=False
    )

    # Build the student check-in address.
    check_in_path = reverse(
        'qr_check_in',
        kwargs={
            'qr_token': classroom.qr_token
        }
    )

    check_in_url = request.build_absolute_uri(check_in_path)

    # Generate QR image.
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
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
        format="PNG"
    )

    image_buffer.seek(0)

    response = HttpResponse(
        image_buffer.getvalue(),
        content_type='image/png'
    )

    response['Content-Disposition'] = (
        f'inline; filename="classroom_{classroom.id}_qr.png"'
    )

    return response
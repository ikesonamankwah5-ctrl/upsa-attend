import csv
import io
import openpyxl

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from .models import Student
from classrooms.models import Classroom


def is_administrator(user):
    return (
        user.is_superuser
        or user.groups.filter(name="Administrator").exists()
    )


def get_user_classrooms(user):

    if is_administrator(user):
        return Classroom.objects.filter(is_archived=False)

    return Classroom.objects.filter(
        Q(lecturers=user) | Q(course_representatives=user),
        is_archived=False
    ).distinct()


@login_required
def student_list(request):

    classrooms = get_user_classrooms(request.user)

    if request.method == 'POST':

        classroom_id = request.POST.get('classroom')
        full_name = request.POST.get('full_name')
        index_number = request.POST.get('index_number')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        classroom = classrooms.filter(id=classroom_id).first()

        if not classroom:
            messages.error(
                request,
                'Please select a valid active classroom.'
            )
            return redirect('student_list')

        if Student.objects.filter(index_number=index_number).exists():
            messages.error(
                request,
                'This index number already exists.'
            )
            return redirect('student_list')

        Student.objects.create(
            classroom=classroom,
            full_name=full_name,
            index_number=index_number,
            email=email,
            phone_number=phone_number
        )

        messages.success(
            request,
            'Student registered successfully!'
        )
        return redirect('student_list')

    students = Student.objects.filter(
        classroom__in=classrooms
    )

    return render(request, 'students/student_list.html', {
        'students': students,
        'classrooms': classrooms
    })


@login_required
def bulk_import_students(request):

    classrooms = get_user_classrooms(request.user)

    if request.method == 'POST':

        classroom_id = request.POST.get('classroom')
        programme_type = request.POST.get('programme_type')
        uploaded_file = request.FILES.get('student_file')

        classroom = classrooms.filter(id=classroom_id).first()

        if not classroom:
            messages.error(
                request,
                'Please select a valid active classroom.'
            )
            return redirect('student_list')

        valid_programme_types = [
            Classroom.DIPLOMA,
            Classroom.UNDERGRADUATE
        ]

        if programme_type not in valid_programme_types:
            messages.error(
                request,
                'Please select a valid programme type.'
            )
            return redirect('student_list')

        # Prevent lecturers and representatives from changing
        # an already assigned programme type.
        if (
            classroom.programme_type
            and classroom.programme_type != programme_type
            and not is_administrator(request.user)
        ):
            messages.error(
                request,
                'You cannot change the programme type assigned to this classroom. '
                'Please contact an administrator.'
            )
            return redirect('student_list')

        if not uploaded_file:
            messages.error(
                request,
                'Please upload a file.'
            )
            return redirect('student_list')

        file_name = uploaded_file.name.lower()

        try:
            rows = []

            # EXCEL IMPORT
            if file_name.endswith('.xlsx'):

                workbook = openpyxl.load_workbook(
                    uploaded_file,
                    read_only=True,
                    data_only=True
                )

                sheet = workbook.active

                header_row = None
                name_position = None
                index_position = None
                standard_format = False

                for row_number, row in enumerate(
                    sheet.iter_rows(values_only=True),
                    start=1
                ):

                    headers = [
                        str(value).strip().lower()
                        if value is not None else ''
                        for value in row
                    ]

                    if (
                        'name of student' in headers
                        and 'index no.' in headers
                    ):
                        header_row = row_number
                        name_position = headers.index(
                            'name of student'
                        )
                        index_position = headers.index(
                            'index no.'
                        )
                        break

                    elif (
                        'full_name' in headers
                        and 'index_number' in headers
                    ):
                        header_row = row_number
                        name_position = headers.index('full_name')
                        index_position = headers.index('index_number')
                        standard_format = True
                        break

                if header_row is None:
                    workbook.close()

                    messages.error(
                        request,
                        'Could not find the required student headings.'
                    )
                    return redirect('student_list')

                for row in sheet.iter_rows(
                    min_row=header_row + 1,
                    values_only=True
                ):

                    if standard_format:
                        name_parts = [
                            str(row[name_position]).strip()
                            if name_position < len(row)
                            and row[name_position] is not None
                            else ''
                        ]

                    else:
                        name_parts = [
                            str(value).strip()
                            for value in row[
                                name_position:name_position + 3
                            ]
                            if value is not None and str(value).strip()
                        ]

                    full_name = ' '.join(name_parts)

                    index_number = (
                        row[index_position]
                        if index_position < len(row) else None
                    )

                    rows.append((full_name, index_number))

                workbook.close()

            # CSV IMPORT
            elif file_name.endswith('.csv'):

                file_data = uploaded_file.read().decode('utf-8-sig')
                csv_file = csv.DictReader(io.StringIO(file_data))

                if not csv_file.fieldnames:
                    messages.error(
                        request,
                        'The CSV file is empty.'
                    )
                    return redirect('student_list')

                cleaned_headers = {
                    heading.strip().lower()
                    for heading in csv_file.fieldnames
                    if heading
                }

                if {
                    'name of student',
                    'index no.'
                }.issubset(cleaned_headers):

                    name_heading = 'name of student'
                    index_heading = 'index no.'

                elif {
                    'full_name',
                    'index_number'
                }.issubset(cleaned_headers):

                    name_heading = 'full_name'
                    index_heading = 'index_number'

                else:
                    messages.error(
                        request,
                        'CSV must contain NAME OF STUDENT and INDEX NO. headings.'
                    )
                    return redirect('student_list')

                for row in csv_file:

                    cleaned_row = {
                        key.strip().lower(): value
                        for key, value in row.items()
                        if key
                    }

                    rows.append((
                        cleaned_row.get(name_heading),
                        cleaned_row.get(index_heading)
                    ))

            else:
                messages.error(
                    request,
                    'Only Excel (.xlsx) and CSV (.csv) files are supported.'
                )
                return redirect('student_list')

            # ASSIGN PROGRAMME TYPE TO CLASSROOM
            if classroom.programme_type != programme_type:

                classroom.programme_type = programme_type
                classroom.save(update_fields=['programme_type'])

            # IMPORT STUDENTS INTO DATABASE
            imported = 0
            skipped = 0

            for full_name, index_number in rows:

                if full_name is None or index_number is None:
                    skipped += 1
                    continue

                full_name = str(full_name).strip()
                index_number = str(index_number).strip()

                if index_number.endswith('.0'):
                    index_number = index_number[:-2]

                if not full_name or not index_number:
                    skipped += 1
                    continue

                if Student.objects.filter(
                    index_number=index_number
                ).exists():
                    skipped += 1
                    continue

                Student.objects.create(
                    classroom=classroom,
                    full_name=full_name,
                    index_number=index_number,
                    email='',
                    phone_number=''
                )

                imported += 1

            messages.success(
                request,
                f'{imported} students imported successfully. '
                f'{skipped} rows skipped.'
            )

        except (
            UnicodeDecodeError,
            csv.Error,
            ValueError,
            OSError
        ):
            messages.error(
                request,
                'The uploaded file could not be read. Please check the file.'
            )

        return redirect('student_list')

    return redirect('student_list')
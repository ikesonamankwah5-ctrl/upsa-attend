from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from students.models import Student
from .models import SemesterResult


def get_classification(cgpa, programme_type):

    if programme_type == 'UNDERGRADUATE':

        if cgpa >= Decimal('3.60'):
            return 'First Class Honours'

        elif cgpa >= Decimal('3.00'):
            return 'Second Class Honours (Upper Division)'

        elif cgpa >= Decimal('2.50'):
            return 'Second Class Honours (Lower Division)'

        elif cgpa >= Decimal('2.00'):
            return 'Third Class Honours'

        elif cgpa >= Decimal('1.00'):
            return 'Pass'

        return 'Fail'

    elif programme_type == 'DIPLOMA':

        if cgpa >= Decimal('3.50'):
            return 'Distinction'

        elif cgpa >= Decimal('2.50'):
            return 'Credit'

        elif cgpa >= Decimal('1.00'):
            return 'Pass'

        return 'Fail'

    return 'Programme type not assigned'


def get_recommended_target(cgpa, programme_type, has_results):

    if not has_results:
        return {
            'target_class': 'Not available yet',
            'target_cgpa': None,
            'target_message': (
                'Enter your semester results to receive '
                'a recommended academic target.'
            )
        }

    if programme_type == 'UNDERGRADUATE':

        targets = [
            (Decimal('2.00'), 'Third Class Honours'),
            (Decimal('2.50'), 'Second Class Honours (Lower Division)'),
            (Decimal('3.00'), 'Second Class Honours (Upper Division)'),
            (Decimal('3.60'), 'First Class Honours'),
        ]

    elif programme_type == 'DIPLOMA':

        targets = [
            (Decimal('1.00'), 'Pass'),
            (Decimal('2.50'), 'Credit'),
            (Decimal('3.50'), 'Distinction'),
        ]

    else:
        return {
            'target_class': 'Programme type not assigned',
            'target_cgpa': None,
            'target_message': (
                'Your classroom programme type must be assigned '
                'before we can recommend an academic target.'
            )
        }

    for threshold, classification in targets:

        if cgpa < threshold:

            return {
                'target_class': classification,
                'target_cgpa': threshold,
                'target_message': (
                    f'Aim for a final CGPA of at least '
                    f'{threshold:.2f} to achieve {classification}.'
                )
            }

    highest_threshold, highest_class = targets[-1]

    return {
        'target_class': highest_class,
        'target_cgpa': highest_threshold,
        'target_message': (
            f'You are currently on track for {highest_class}. '
            f'Maintain or improve your performance.'
        )
    }


def get_target_options(programme_type):

    if programme_type == 'UNDERGRADUATE':
        return [
            {
                'value': '2.00',
                'label': 'Third Class Honours (2.00)'
            },
            {
                'value': '2.50',
                'label': 'Second Class Honours - Lower Division (2.50)'
            },
            {
                'value': '3.00',
                'label': 'Second Class Honours - Upper Division (3.00)'
            },
            {
                'value': '3.60',
                'label': 'First Class Honours (3.60)'
            },
        ]

    elif programme_type == 'DIPLOMA':
        return [
            {
                'value': '1.00',
                'label': 'Pass (1.00)'
            },
            {
                'value': '2.50',
                'label': 'Credit (2.50)'
            },
            {
                'value': '3.50',
                'label': 'Distinction (3.50)'
            },
        ]

    return []


def calculate_target_gpa(
    current_cgpa,
    completed_credits,
    remaining_credits,
    target_cgpa
):

    total_credits = completed_credits + remaining_credits

    required_quality_points = target_cgpa * total_credits

    current_quality_points = current_cgpa * completed_credits

    required_gpa = (
        required_quality_points - current_quality_points
    ) / remaining_credits

    if required_gpa > Decimal('4.00'):
        return {
            'achievable': False,
            'required_gpa': required_gpa.quantize(Decimal('0.01')),
            'message': (
                'This target is currently not achievable '
                'with the remaining credit hours because '
                'the required GPA exceeds 4.00.'
            )
        }

    if required_gpa <= Decimal('0'):
        return {
            'achievable': True,
            'required_gpa': Decimal('0.00'),
            'message': (
                'You have already secured this target based '
                'on the credits and results entered. Maintain '
                'your performance.'
            )
        }

    return {
        'achievable': True,
        'required_gpa': required_gpa.quantize(Decimal('0.01')),
        'message': (
            'This target is mathematically achievable. '
            'Aim to maintain at least this average GPA '
            'over your remaining credit hours.'
        )
    }


def calculate_semester_gpa(
    current_cgpa,
    completed_credits,
    semester_credits,
    target_cgpa
):

    return calculate_target_gpa(
        current_cgpa,
        completed_credits,
        semester_credits,
        target_cgpa
    )


@login_required
def cgpa_dashboard(request):

    try:
        student = Student.objects.select_related(
            'classroom'
        ).get(user=request.user)

    except Student.DoesNotExist:
        messages.error(
            request,
            'Your account is not linked to a student profile.'
        )
        return redirect('dashboard')

    results = SemesterResult.objects.filter(student=student)

    cgpa = SemesterResult.calculate_cgpa(student)

    total_credits = sum(
        (result.credit_hours for result in results),
        Decimal('0')
    )

    has_results = results.exists()

    if has_results:
        classification = get_classification(
            cgpa,
            student.classroom.programme_type
        )
    else:
        classification = 'Not available yet'

    recommendation = get_recommended_target(
        cgpa,
        student.classroom.programme_type,
        has_results
    )

    target_options = get_target_options(
        student.classroom.programme_type
    )

    target_result = None
    semester_gpa_result = None

    if request.method == 'POST':

        action = request.POST.get('action', 'add_semester')

        # TARGET CLASS CALCULATOR

        if action == 'calculate_target':

            target_value = request.POST.get(
                'target_cgpa', ''
            ).strip()

            remaining_value = request.POST.get(
                'remaining_credits', ''
            ).strip()

            if not target_value or not remaining_value:
                messages.error(
                    request,
                    'Please select a target class and enter your remaining credit hours.'
                )

            elif not has_results or total_credits <= 0:
                messages.error(
                    request,
                    'Please enter your completed semester results before calculating a target.'
                )

            else:

                try:
                    target_cgpa = Decimal(target_value)
                    remaining_credits = Decimal(remaining_value)

                    valid_targets = [
                        Decimal(option['value'])
                        for option in target_options
                    ]

                    if target_cgpa not in valid_targets:
                        raise ValueError

                    if not remaining_credits.is_finite():
                        raise ValueError

                    if remaining_credits <= 0:
                        raise ValueError

                    target_result = calculate_target_gpa(
                        cgpa,
                        total_credits,
                        remaining_credits,
                        target_cgpa
                    )

                    target_result['target_cgpa'] = target_cgpa
                    target_result['remaining_credits'] = remaining_credits

                except (InvalidOperation, ValueError):
                    messages.error(
                        request,
                        'Please enter valid target and credit hour values.'
                    )

        # REQUIRED SEMESTER GPA CALCULATOR

        elif action == 'calculate_semester_gpa':

            target_value = request.POST.get(
                'semester_target_cgpa', ''
            ).strip()

            credit_value = request.POST.get(
                'semester_credits', ''
            ).strip()

            if not target_value or not credit_value:
                messages.error(
                    request,
                    'Please enter your target CGPA and upcoming semester credit hours.'
                )

            elif not has_results or total_credits <= 0:
                messages.error(
                    request,
                    'Please add your completed semester results first.'
                )

            else:

                try:
                    target_cgpa = Decimal(target_value)
                    semester_credits = Decimal(credit_value)

                    if not target_cgpa.is_finite():
                        raise ValueError

                    if not semester_credits.is_finite():
                        raise ValueError

                    if target_cgpa <= 0 or target_cgpa > 4:
                        raise ValueError

                    if semester_credits <= 0:
                        raise ValueError

                    semester_gpa_result = calculate_semester_gpa(
                        cgpa,
                        total_credits,
                        semester_credits,
                        target_cgpa
                    )

                    semester_gpa_result['target_cgpa'] = target_cgpa
                    semester_gpa_result['semester_credits'] = semester_credits

                except (InvalidOperation, ValueError):
                    messages.error(
                        request,
                        'Please enter valid target CGPA and credit hour values.'
                    )

        # ADD SEMESTER RESULT

        else:

            academic_year = request.POST.get(
                'academic_year', ''
            ).strip()

            semester_name = request.POST.get(
                'semester_name', ''
            ).strip()

            gpa_value = request.POST.get('gpa', '').strip()

            credit_value = request.POST.get(
                'credit_hours', ''
            ).strip()

            if not all([
                academic_year,
                semester_name,
                gpa_value,
                credit_value
            ]):
                messages.error(
                    request,
                    'Please complete all fields.'
                )
                return redirect('cgpa_dashboard')

            try:
                semester_gpa = Decimal(gpa_value)
                credit_hours = Decimal(credit_value)

                if not semester_gpa.is_finite():
                    raise ValueError

                if not credit_hours.is_finite():
                    raise ValueError

                if semester_gpa < 0 or semester_gpa > 4:
                    messages.error(
                        request,
                        'GPA must be between 0.00 and 4.00.'
                    )
                    return redirect('cgpa_dashboard')

                if credit_hours <= 0:
                    messages.error(
                        request,
                        'Credit hours must be greater than zero.'
                    )
                    return redirect('cgpa_dashboard')

                if len(academic_year) > 20 or len(semester_name) > 50:
                    messages.error(
                        request,
                        'Please check the academic year and semester name.'
                    )
                    return redirect('cgpa_dashboard')

                with transaction.atomic():

                    SemesterResult.objects.create(
                        student=student,
                        academic_year=academic_year,
                        semester_name=semester_name,
                        gpa=semester_gpa,
                        credit_hours=credit_hours
                    )

                messages.success(
                    request,
                    'Semester result added successfully!'
                )

                return redirect('cgpa_dashboard')

            except (InvalidOperation, ValueError, ValidationError):
                messages.error(
                    request,
                    'Please enter valid numerical values.'
                )

            except IntegrityError:
                messages.error(
                    request,
                    'A result for this academic year and semester already exists.'
                )

            return redirect('cgpa_dashboard')

    return render(
        request,
        'gpa/cgpa_dashboard.html',
        {
            'student': student,
            'results': results,
            'cgpa': cgpa,
            'total_credits': total_credits,
            'classification': classification,
            'recommendation': recommendation,
            'target_options': target_options,
            'target_result': target_result,
            'semester_gpa_result': semester_gpa_result,
        }
    )
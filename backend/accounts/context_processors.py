def user_roles(request):
    if not request.user.is_authenticated:
        return {
            'is_administrator': False,
            'is_lecturer': False,
            'is_course_representative': False,
            'is_student': False,
        }

    user = request.user

    return {
        'is_administrator': (
            user.is_superuser
            or user.groups.filter(name='Administrator').exists()
        ),
        'is_lecturer': user.groups.filter(name='Lecturer').exists(),
        'is_course_representative': user.groups.filter(
            name='Course Representative'
        ).exists(),
        'is_student': hasattr(user, 'student_profile'),
    }
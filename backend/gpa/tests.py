from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from classrooms.models import Classroom
from students.models import Student
from .models import SemesterResult


User = get_user_model()


class GPAPrivacyTests(TestCase):

    def setUp(self):

        # Create two separate student accounts
        self.student_user = User.objects.create_user(
            username='student_one',
            password='TestPassword123'
        )

        self.other_student_user = User.objects.create_user(
            username='student_two',
            password='TestPassword123'
        )

        # Create classroom
        self.classroom = Classroom.objects.create(
            name='Business Administration 300',
            programme='Business Administration',
            programme_type='UNDERGRADUATE',
            level=300,
            academic_year='2026/2027',
            created_by=self.student_user
        )

        # Create student profiles
        self.student = Student.objects.create(
            user=self.student_user,
            classroom=self.classroom,
            full_name='Student One',
            index_number='TEST001'
        )

        self.other_student = Student.objects.create(
            user=self.other_student_user,
            classroom=self.classroom,
            full_name='Student Two',
            index_number='TEST002'
        )

        # Create private GPA records
        self.own_result = SemesterResult.objects.create(
            student=self.student,
            academic_year='2026/2027',
            semester_name='First Semester',
            gpa='3.50',
            credit_hours='15'
        )

        self.other_result = SemesterResult.objects.create(
            student=self.other_student,
            academic_year='2026/2027',
            semester_name='First Semester',
            gpa='2.50',
            credit_hours='15'
        )

        self.dashboard_url = reverse('cgpa_dashboard')

    def test_student_can_access_own_gpa(self):

        self.client.login(
            username='student_one',
            password='TestPassword123'
        )

        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, 200)

        results = list(response.context['results'])

        self.assertIn(self.own_result, results)

    def test_student_cannot_see_another_students_gpa(self):

        self.client.login(
            username='student_one',
            password='TestPassword123'
        )

        response = self.client.get(self.dashboard_url)

        results = list(response.context['results'])

        self.assertIn(self.own_result, results)
        self.assertNotIn(self.other_result, results)

    def test_administrator_cannot_access_gpa_dashboard(self):

        admin = User.objects.create_superuser(
            username='test_admin',
            email='admin@example.com',
            password='AdminPassword123'
        )

        self.client.login(
            username='test_admin',
            password='AdminPassword123'
        )

        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            response.url,
            reverse('dashboard')
        )

    def test_unauthenticated_user_cannot_access_gpa(self):

        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)
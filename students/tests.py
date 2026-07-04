from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Student

User = get_user_model()


class StudentTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="student1",
            password="test123",
            role="STUDENT"
        )

        self.student = Student.objects.create(
            user=self.user,
            full_name="Test Student",
            national_id="12345678",
            gender="Male",
            institution="Test University",
            course="Computer Science",
            duration="3 months",
            start_date="2026-01-01",
            end_date="2026-04-01",
            training_mode="ONLINE",
            session="MORNING",
            status="PENDING"
        )

    def test_student_creation(self):

        self.assertEqual(self.student.full_name, "Test Student")
        self.assertEqual(self.student.status, "PENDING")
from django.test import TestCase
from django.contrib.auth import get_user_model
from students.models import Student
from .models import LogbookEntry
from datetime import date


User = get_user_model()


class LogbookTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="student1",
            password="test1234",
            role="STUDENT"
        )

        self.student = Student.objects.create(user=self.user)

    def test_create_logbook_entry(self):

        entry = LogbookEntry.objects.create(
            student=self.student,
            title="Day 1",
            description="Intro",
            work_done="Setup environment",
            date=date.today()
        )

        self.assertEqual(entry.student, self.student)
        self.assertEqual(entry.status, "PENDING")
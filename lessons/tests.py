from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Lesson

User = get_user_model()


class LessonTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="trainer1",
            password="test123",
            role="TRAINER"
        )

        self.lesson = Lesson.objects.create(
            title="Intro to ICT",
            lesson_code="ICT101",
            description="Basic ICT concepts",
            created_by=self.user,
            status="PUBLISHED"
        )

    def test_lesson_creation(self):

        self.assertEqual(self.lesson.title, "Intro to ICT")
        self.assertEqual(self.lesson.status, "PUBLISHED")
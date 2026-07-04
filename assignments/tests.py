from django.test import TestCase
from django.utils import timezone

from accounts.models import User

from .models import (
    Assignment,
    AssignmentSubmission
)


class AssignmentModelTest(TestCase):

    def setUp(self):

        self.trainer = User.objects.create_user(
            username='trainer1',
            password='password123',
            role='TRAINER'
        )

    def test_assignment_creation(self):

        assignment = Assignment.objects.create(
            title='Python Basics',
            assignment_code='ASS001',
            instructions='Complete the exercise',
            total_marks=100,
            due_date=timezone.now(),
            created_by=self.trainer
        )

        self.assertEqual(
            assignment.title,
            'Python Basics'
        )


class SubmissionModelTest(TestCase):

    def setUp(self):

        self.trainer = User.objects.create_user(
            username='trainer1',
            password='password123',
            role='TRAINER'
        )

        self.student = User.objects.create_user(
            username='student1',
            password='password123',
            role='STUDENT'
        )

        self.assignment = Assignment.objects.create(
            title='Python Basics',
            assignment_code='ASS001',
            instructions='Do work',
            total_marks=100,
            due_date=timezone.now(),
            created_by=self.trainer
        )

    def test_submission_creation(self):

        submission = AssignmentSubmission.objects.create(
            assignment=self.assignment,
            student=self.student,
            submission_file='test.pdf'
        )

        self.assertEqual(
            submission.student.username,
            'student1'
        )
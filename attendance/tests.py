from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import AttendanceSession, AttendanceRecord

User = get_user_model()


class AttendanceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="student1",
            password="test123"
        )

        self.session = AttendanceSession.objects.create(
            title="Test Session",
            qr_code="test-qrcode-123"
        )

    def test_attendance_creation(self):
        record = AttendanceRecord.objects.create(
            session=self.session,
            user=self.user
        )

        self.assertEqual(record.session, self.session)
        self.assertEqual(record.user, self.user)
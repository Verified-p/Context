# accounts/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import EmailVerification

User = get_user_model()


# =====================================================
# USER MODEL TESTS
# =====================================================

class UserModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='STUDENT'
        )

    def test_user_creation(self):

        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.role, 'STUDENT')
        self.assertFalse(self.user.is_locked)

    def test_email_verification_created(self):

        verification = EmailVerification.objects.filter(
            user=self.user
        ).first()

        self.assertIsNotNone(verification)


# =====================================================
# LOGIN TESTS
# =====================================================

class LoginTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='loginuser',
            email='login@example.com',
            password='loginpass123',
            role='TRAINER'
        )

    def test_login_success(self):

        response = self.client.post(
            reverse('accounts:login'),
            {
                'username': 'loginuser',
                'password': 'loginpass123'
            }
        )

        self.assertEqual(response.status_code, 302)  # redirect after login


# =====================================================
# ROLE TESTS
# =====================================================

class RoleTest(TestCase):

    def setUp(self):

        self.admin = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpass123',
            role='SUPER_ADMIN'
        )

    def test_role_assignment(self):

        self.assertTrue(self.admin.role == 'SUPER_ADMIN')


# =====================================================
# ACCOUNT LOCK TESTS
# =====================================================

class AccountLockTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='lockeduser',
            email='locked@example.com',
            password='testpass123',
            role='STUDENT'
        )

    def test_lock_user(self):

        self.user.is_locked = True
        self.user.save()

        self.assertTrue(self.user.is_locked)


# =====================================================
# PROFILE UPDATE TEST
# =====================================================

class ProfileUpdateTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='profileuser',
            email='profile@example.com',
            password='testpass123',
            role='STUDENT'
        )

    def test_profile_update(self):

        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.user.save()

        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
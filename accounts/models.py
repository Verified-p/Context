# accounts/models.py

import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Main User Model for CETMS
    """

    ROLE_CHOICES = (
        ('SUPER_ADMIN', 'Super Admin'),
        ('TRAINER', 'Trainer'),
        ('STUDENT', 'Student'),
        ('FINANCE', 'Finance Officer'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='STUDENT'
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    last_seen = models.DateTimeField(
        blank=True,
        null=True
    )

    failed_login_attempts = models.PositiveIntegerField(
        default=0
    )

    is_locked = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-date_joined']
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_super_admin(self):
        return self.role == "SUPER_ADMIN"

    @property
    def is_trainer(self):
        return self.role == "TRAINER"

    @property
    def is_student(self):
        return self.role == "STUDENT"

    @property
    def is_finance(self):
        return self.role == "FINANCE"

    def update_last_seen(self):
        self.last_seen = timezone.now()
        self.save(update_fields=['last_seen'])


class EmailVerification(models.Model):
    """
    Email verification token
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='email_verification'
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    verified_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.email


class LoginActivity(models.Model):
    """
    Audit login activity
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='login_activities'
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True
    )

    browser = models.TextField(
        blank=True,
        null=True
    )

    login_time = models.DateTimeField(
        auto_now_add=True
    )

    success = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"


class AuditLog(models.Model):
    """
    System audit logs
    """

    ACTION_CHOICES = (
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('APPROVE', 'Approve'),
        ('REJECT', 'Reject'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )

    description = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} - {self.timestamp}"
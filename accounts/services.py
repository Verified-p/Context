# accounts/services.py

from django.utils import timezone
from django.db import transaction

from .models import (
    User,
    EmailVerification,
    LoginActivity,
    AuditLog
)


class UserService:
    """
    User Business Logic
    """

    MAX_FAILED_ATTEMPTS = 5

    # ==========================================
    # CREATE USER (TRAINER / FINANCE / ADMIN)
    # ==========================================

    @staticmethod
    @transaction.atomic
    def create_user(form):

        user = form.save()

        EmailVerification.objects.create(
            user=user
        )

        AuditLog.objects.create(
            user=user,
            action="CREATE",
            description=f"User account created: {user.username}"
        )

        return user

    # ==========================================
    # CREATE STUDENT ACCOUNT
    # ==========================================

    @staticmethod
    @transaction.atomic
    def create_student_account(student):

        """
        Creates login credentials automatically
        Username = Admission Number
        Password = National ID
        """

        username = student.admission_number.strip()

        password = student.national_id.strip()

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=student.full_name,
            email=student.email,
            phone_number=student.phone_number,
            role="STUDENT",
            is_active=True
        )

        EmailVerification.objects.create(
            user=user
        )

        AuditLog.objects.create(
            user=user,
            action="CREATE",
            description=(
                f"Student account created "
                f"for {student.full_name}"
            )
        )

        return user

    # ==========================================
    # ACTIVATE USER
    # ==========================================

    @staticmethod
    def activate_user(user):

        user.is_active = True

        user.save(
            update_fields=["is_active"]
        )

        AuditLog.objects.create(
            user=user,
            action="UPDATE",
            description="Account activated"
        )

    # ==========================================
    # DEACTIVATE USER
    # ==========================================

    @staticmethod
    def deactivate_user(user):

        user.is_active = False

        user.save(
            update_fields=["is_active"]
        )

        AuditLog.objects.create(
            user=user,
            action="UPDATE",
            description="Account deactivated"
        )

    # ==========================================
    # LOCK USER
    # ==========================================

    @staticmethod
    def lock_user(user):

        user.is_locked = True

        user.save(
            update_fields=["is_locked"]
        )

        AuditLog.objects.create(
            user=user,
            action="UPDATE",
            description="Account locked"
        )

    # ==========================================
    # UNLOCK USER
    # ==========================================

    @staticmethod
    def unlock_user(user):

        user.is_locked = False

        user.failed_login_attempts = 0

        user.save(
            update_fields=[
                "is_locked",
                "failed_login_attempts"
            ]
        )

        AuditLog.objects.create(
            user=user,
            action="UPDATE",
            description="Account unlocked"
        )

    # ==========================================
    # RESET PASSWORD
    # ==========================================

    @staticmethod
    def reset_password(user, password):

        user.set_password(password)

        user.save()

        AuditLog.objects.create(
            user=user,
            action="UPDATE",
            description="Password reset"
        )

    # ==========================================
    # FAILED LOGIN
    # ==========================================

    @staticmethod
    def register_failed_login(user):

        user.failed_login_attempts += 1

        if (
            user.failed_login_attempts >=
            UserService.MAX_FAILED_ATTEMPTS
        ):
            user.is_locked = True

        user.save()

    # ==========================================
    # LAST SEEN
    # ==========================================

    @staticmethod
    def update_last_seen(user):

        user.last_seen = timezone.now()

        user.save(
            update_fields=[
                "last_seen"
            ]
        )


# ==========================================
# EMAIL VERIFICATION
# ==========================================

class EmailVerificationService:

    @staticmethod
    def verify_user(token):

        try:

            verification = (
                EmailVerification.objects.get(
                    token=token
                )
            )

            verification.is_verified = True

            verification.verified_at = (
                timezone.now()
            )

            verification.save()

            verification.user.is_verified = True

            verification.user.save(
                update_fields=[
                    "is_verified"
                ]
            )

            return True

        except EmailVerification.DoesNotExist:

            return False


# ==========================================
# LOGIN ACTIVITY
# ==========================================

class LoginActivityService:

    @staticmethod
    def create_log(
        user,
        request,
        success=True
    ):

        ip_address = request.META.get(
            "REMOTE_ADDR"
        )

        browser = request.META.get(
            "HTTP_USER_AGENT",
            ""
        )

        LoginActivity.objects.create(
            user=user,
            ip_address=ip_address,
            browser=browser,
            success=success
        )


# ==========================================
# AUDIT SERVICE
# ==========================================

class AuditService:

    @staticmethod
    def log(
        user,
        action,
        description
    ):

        AuditLog.objects.create(
            user=user,
            action=action,
            description=description
        )
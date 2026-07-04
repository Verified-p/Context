# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out
)

from django.utils import timezone

from .models import (
    User,
    EmailVerification,
    AuditLog,
    LoginActivity
)


# ==========================================
# CREATE EMAIL VERIFICATION AUTOMATICALLY
# ==========================================

@receiver(post_save, sender=User)
def create_email_verification(
    sender,
    instance,
    created,
    **kwargs
):
    """
    Automatically create
    EmailVerification record
    for every new user.
    """

    if created:

        EmailVerification.objects.get_or_create(
            user=instance
        )


# ==========================================
# USER LOGIN
# ==========================================

@receiver(user_logged_in)
def user_logged_in_handler(
    sender,
    request,
    user,
    **kwargs
):
    """
    Actions performed after login.
    """

    # Reset lock counters
    user.failed_login_attempts = 0
    user.is_locked = False

    # Update last seen
    user.last_seen = timezone.now()

    user.save(
        update_fields=[
            'failed_login_attempts',
            'is_locked',
            'last_seen'
        ]
    )

    # Save login activity
    LoginActivity.objects.create(
        user=user,
        ip_address=request.META.get(
            'REMOTE_ADDR'
        ),
        browser=request.META.get(
            'HTTP_USER_AGENT',
            ''
        ),
        success=True
    )

    # Audit log
    AuditLog.objects.create(
        user=user,
        action='LOGIN',
        description='User logged in'
    )


# ==========================================
# USER LOGOUT
# ==========================================

@receiver(user_logged_out)
def user_logged_out_handler(
    sender,
    request,
    user,
    **kwargs
):
    """
    Audit logout events.
    """

    if user:

        AuditLog.objects.create(
            user=user,
            action='LOGOUT',
            description='User logged out'
        )
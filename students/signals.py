# students/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Student


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_student_profile(sender, instance, created, **kwargs):
    """
    Auto-create a Student profile only when a STUDENT account
    is created outside the Student Registration Form.

    Prevents duplicate Student creation.
    """

    if not created:
        return

    if not hasattr(instance, "role"):
        return

    if instance.role != "STUDENT":
        return

    # If a student profile already exists, do nothing
    if Student.objects.filter(user=instance).exists():
        return

    # Since CETMS registers students using the
    # Student Registration Form, we do NOT create
    # a Student record automatically here.
    return
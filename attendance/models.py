from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import uuid


class AttendanceSession(models.Model):
    """
    Attendance session created by a trainer/admin.
    Students can only mark attendance while the session is open.
    """

    title = models.CharField(max_length=255)

    course = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_sessions"
    )

    session_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # Attendance opening time
    opens_at = models.DateTimeField(
        default=timezone.now
    )

    # Default attendance duration (20 minutes)
    duration_minutes = models.PositiveIntegerField(
        default=20
    )

    # Closing time
    expires_at = models.DateTimeField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        if not self.expires_at:
            self.expires_at = (
                self.opens_at +
                timedelta(minutes=self.duration_minutes)
            )

        super().save(*args, **kwargs)

    @property
    def total_attendees(self):
        return self.records.count()

    @property
    def is_open(self):

        now = timezone.now()

        return (
            self.is_active and
            self.opens_at <= now <= self.expires_at
        )

    @property
    def is_expired(self):

        return timezone.now() > self.expires_at

    @property
    def time_remaining(self):

        if self.is_expired:
            return 0

        seconds = int(
            (self.expires_at - timezone.now()).total_seconds()
        )

        return max(seconds, 0)

    def close_session(self):

        self.is_active = False
        self.save(update_fields=["is_active"])

    def __str__(self):
        return self.title


class AttendanceRecord(models.Model):

    STATUS_CHOICES = (
        ("PRESENT", "Present"),
        ("ABSENT", "Absent"),
        ("LATE", "Late"),
    )

    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name="records"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PRESENT"
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["-timestamp"]
        unique_together = (
            "session",
            "student"
        )

    def __str__(self):
        return f"{self.student.username} - {self.session.title}"
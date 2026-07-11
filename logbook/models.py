from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from students.storage import RawMediaCloudinaryStorage

# ==========================================
# STUDENT LOGBOOK FILE
# ==========================================
''


class StudentLogbook(models.Model):
    """
    Student uploads one university logbook.

    The uploaded DOCX becomes the official attachment logbook
    that is updated throughout the attachment period using
    ONLYOFFICE.
    """

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_logbook"
    )

    logbook_file = models.FileField(
        upload_to="logbooks/",
        storage=RawMediaCloudinaryStorage(),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["docx"]
            )
        ]
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_logbooks"
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    # Version number for future document history/versioning
    version = models.PositiveIntegerField(
        default=1
    )

    # Indicates whether the document has unsaved/new changes
    is_updated = models.BooleanField(
        default=False
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Student Logbook"
        verbose_name_plural = "Student Logbooks"

    def __str__(self):
        return (
            f"{self.student.get_full_name() or self.student.username}"
            f" - {self.get_status_display()}"
        )

# ==========================================
# DAILY LOGBOOK ENTRIES
# ==========================================

class LogbookEntry(models.Model):
    """
    Daily activities recorded by the student.
    These entries can later be synchronized with the uploaded DOCX.
    """

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="logbook_entries"
    )

    logbook = models.ForeignKey(
        StudentLogbook,
        on_delete=models.CASCADE,
        related_name="entries"
    )

    attendance_session = models.ForeignKey(
        "attendance.AttendanceSession",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logbook_entries"
    )

    date = models.DateField(
        default=timezone.now
    )

    title = models.CharField(
        max_length=255
    )

    activity = models.TextField()

    reflection = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_logs"
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    score = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-date",
            "-created_at"
        ]

        unique_together = (
            "student",
            "date",
            "title"
        )

    def __str__(self):
        return (
            f"{self.student.username} - "
            f"{self.title} ({self.date})"
        )

    def calculate_score(self):

        score = 0

        if self.activity:

            if len(self.activity) >= 50:
                score += 40
            else:
                score += 20

        if self.reflection:

            if len(self.reflection) >= 50:
                score += 40
            else:
                score += 20

        if self.status == "APPROVED":
            score += 20

        return min(score, 100)

    def save(self, *args, **kwargs):

        self.score = self.calculate_score()

        super().save(*args, **kwargs)
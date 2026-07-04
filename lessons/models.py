from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime


class Lesson(models.Model):

    STATUS = (
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
    )

    LESSON_TYPE = (
        ('RECORDED', 'Recorded Lesson'),
        ('LIVE', 'Live Lesson'),
    )

    title = models.CharField(
        max_length=255
    )

    lesson_code = models.CharField(
        max_length=50,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    lesson_type = models.CharField(
        max_length=20,
        choices=LESSON_TYPE,
        default='RECORDED'
    )

    # ==========================
    # Recorded Lesson Resources
    # ==========================

    video = models.FileField(
        upload_to='lessons/videos/',
        blank=True,
        null=True
    )

    pdf = models.FileField(
        upload_to='lessons/pdfs/',
        blank=True,
        null=True
    )

    recording = models.FileField(
        upload_to='lessons/recordings/',
        blank=True,
        null=True
    )

    # ==========================
    # Live Lesson
    # ==========================

    lesson_date = models.DateField(
        blank=True,
        null=True
    )

    start_time = models.TimeField(
        blank=True,
        null=True
    )

    end_time = models.TimeField(
        blank=True,
        null=True
    )

    meeting_link = models.URLField(
        blank=True,
        null=True,
        help_text="Google Meet, Zoom or Microsoft Teams link."
    )

    # ==========================

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_lessons'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='DRAFT'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            '-lesson_date',
            '-created_at'
        ]

    def __str__(self):
        return self.title

    # ===================================
    # Compatibility Properties
    # ===================================

    @property
    def live_date(self):
        return self.lesson_date

    @property
    def live_time(self):
        return self.start_time

    @property
    def duration_minutes(self):
        if self.start_time and self.end_time:

            start = datetime.combine(
                timezone.now().date(),
                self.start_time
            )

            end = datetime.combine(
                timezone.now().date(),
                self.end_time
            )

            return int((end - start).total_seconds() / 60)

        return None

    @property
    def is_live_today(self):
        return (
            self.lesson_date == timezone.localdate()
        )

    @property
    def has_started(self):
        if not self.lesson_date or not self.start_time:
            return False

        start = timezone.make_aware(
            datetime.combine(
                self.lesson_date,
                self.start_time
            )
        )

        return timezone.now() >= start

    @property
    def has_ended(self):
        if not self.lesson_date or not self.end_time:
            return False

        end = timezone.make_aware(
            datetime.combine(
                self.lesson_date,
                self.end_time
            )
        )

        return timezone.now() >= end


class LessonProgress(models.Model):

    STATUS = (
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lesson_progress'
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='NOT_STARTED'
    )

    joined_live = models.BooleanField(
        default=False
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = (
            'student',
            'lesson'
        )

    def __str__(self):
        return f"{self.student.username} - {self.lesson.title}"
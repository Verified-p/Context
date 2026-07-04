from django.db import models
from django.conf import settings
from django.utils import timezone

from lessons.models import Lesson


class Evaluation(models.Model):
    """
    Trainer evaluation per student per lesson/course
    """

    STATUS_CHOICES = (
        ("DRAFT", "Draft"),
        ("SUBMITTED", "Submitted"),
        ("REVIEWED", "Reviewed"),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="evaluations"
    )

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="given_evaluations"
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="evaluations"
    )

    title = models.CharField(max_length=255)

    technical_score = models.PositiveIntegerField(default=0)
    discipline_score = models.PositiveIntegerField(default=0)
    attendance_score = models.PositiveIntegerField(default=0)
    communication_score = models.PositiveIntegerField(default=0)

    total_score = models.FloatField(default=0)

    feedback = models.TextField(blank=True, null=True)

    period_start = models.DateField(default=timezone.now)
    period_end = models.DateField(default=timezone.now)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DRAFT"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("student", "lesson", "period_start")

    def save(self, *args, **kwargs):
        self.total_score = (
            self.technical_score +
            self.discipline_score +
            self.attendance_score +
            self.communication_score
        ) / 4

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.lesson.title}"
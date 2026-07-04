from django.db import models
from django.conf import settings
from django.utils import timezone

from lessons.models import Lesson


class Assignment(models.Model):
    """
    Assignment created by Trainer or Super Admin
    """

    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('CLOSED', 'Closed'),
    )

    title = models.CharField(
        max_length=255
    )

    assignment_code = models.CharField(
        max_length=50,
        unique=True
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='assignments',
        null=True,
        blank=True
    )

    instructions = models.TextField()

    attachment = models.FileField(
        upload_to='assignments/questions/',
        blank=True,
        null=True
    )

    total_marks = models.PositiveIntegerField(
        default=100
    )

    due_date = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_assignments'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        return timezone.now() > self.due_date

    @property
    def total_submissions(self):
        return self.submissions.count()


class AssignmentSubmission(models.Model):
    """
    Student Assignment Submission
    """

    STATUS_CHOICES = (
        ('SUBMITTED', 'Submitted'),
        ('GRADED', 'Graded'),
    )

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions'
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assignment_submissions'
    )

    submission_file = models.FileField(
        upload_to='assignments/submissions/'
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    is_late = models.BooleanField(
        default=False
    )

    marks_awarded = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    feedback = models.TextField(
        blank=True,
        null=True
    )

    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='graded_assignments'
    )

    graded_at = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='SUBMITTED'
    )

    class Meta:
        ordering = ['-submitted_at']
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

    def save(self, *args, **kwargs):

        if self.assignment and self.assignment.due_date:
            self.is_late = timezone.now() > self.assignment.due_date

        super().save(*args, **kwargs)

    @property
    def percentage_score(self):

        if not self.marks_awarded:
            return 0

        return round(
            (float(self.marks_awarded) / self.assignment.total_marks) * 100,
            2
        )
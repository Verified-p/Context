# notifications/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone


class Notification(models.Model):
    """
    Main notification model.

    This model is used throughout CETMS to notify users about:
    - Lessons
    - Assignments
    - Assignment submissions
    - Attendance
    - Logbooks
    - Certificates
    - Reports
    - Finance
    - User management
    - General system events
    """

    TYPE_CHOICES = (

        ("SYSTEM", "System"),

        ("LESSON", "Lesson"),

        ("ASSIGNMENT", "Assignment"),

        ("SUBMISSION", "Submission"),

        ("ATTENDANCE", "Attendance"),

        ("LOGBOOK", "Logbook"),

        ("CERTIFICATE", "Certificate"),

        ("USER", "User"),

        ("REPORT", "Report"),

        ("FINANCE", "Finance"),

        ("GENERAL", "General"),

    )

    PRIORITY_CHOICES = (

        ("LOW", "Low"),

        ("NORMAL", "Normal"),

        ("HIGH", "High"),

        ("URGENT", "Urgent"),

    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_notifications"
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        default="GENERAL"
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="NORMAL"
    )

    icon = models.CharField(
        max_length=50,
        default="fa-bell",
        help_text="Font Awesome icon."
    )

    color = models.CharField(
        max_length=30,
        default="primary",
        help_text="Bootstrap color."
    )

    action_text = models.CharField(
        max_length=100,
        default="View",
        blank=True
    )

    url = models.CharField(
        max_length=500,
        blank=True,
        default=""
    )

    is_read = models.BooleanField(
        default=False
    )

    is_archived = models.BooleanField(
        default=False
    )

    is_deleted = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    read_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

        indexes = [

            models.Index(
                fields=[
                    "recipient",
                    "is_read"
                ]
            ),

            models.Index(
                fields=[
                    "notification_type"
                ]
            ),

            models.Index(
                fields=[
                    "created_at"
                ]
            ),

        ]

    def __str__(self):

        return f"{self.recipient.username} - {self.title}"

    @property
    def unread(self):

        return not self.is_read

    @property
    def time_since(self):

        return timezone.localtime(
            self.created_at
        )

    def mark_as_read(self):

        """
        Mark notification as read.
        """

        if not self.is_read:

            self.is_read = True

            self.read_at = timezone.now()

            self.save(
                update_fields=[
                    "is_read",
                    "read_at"
                ]
            )

    def archive(self):

        """
        Archive notification.
        """

        if not self.is_archived:

            self.is_archived = True

            self.save(
                update_fields=[
                    "is_archived"
                ]
            )

    def soft_delete(self):

        """
        Soft delete notification.
        """

        if not self.is_deleted:

            self.is_deleted = True

            self.save(
                update_fields=[
                    "is_deleted"
                ]
            )



class Announcement(models.Model):
    """
    System announcements.

    Announcements are visible to users based on their role.
    Example:
    - All users
    - Students only
    - Trainers only
    - Finance only
    - Super Admin only
    """

    ROLE_CHOICES = (

        ("ALL", "All Users"),

        ("SUPER_ADMIN", "Super Admin"),

        ("TRAINER", "Trainer"),

        ("STUDENT", "Student"),

        ("FINANCE", "Finance"),

    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    target_role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default="ALL"
    )

    priority = models.CharField(
        max_length=20,
        choices=Notification.PRIORITY_CHOICES,
        default="NORMAL"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_announcements"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

    def __str__(self):

        return self.title

    @property
    def expired(self):
        """
        Returns True if the announcement has expired.
        """

        if not self.expires_at:
            return False

        return timezone.now() > self.expires_at

    @property
    def is_visible(self):
        """
        Returns True if the announcement should currently be shown.
        """

        if not self.is_active:
            return False

        if self.expires_at:

            return timezone.now() <= self.expires_at

        return True

    def deactivate(self):
        """
        Hide the announcement without deleting it.
        """

        if self.is_active:

            self.is_active = False

            self.save(
                update_fields=[
                    "is_active"
                ]
            )

    def activate(self):
        """
        Make the announcement visible again.
        """

        if not self.is_active:

            self.is_active = True

            self.save(
                update_fields=[
                    "is_active"
                ]
            )


class Reminder(models.Model):
    """
    Personal reminders.

    Reminders are created for individual users to remind them about
    upcoming deadlines, attendance sessions, assignment due dates,
    meetings, logbook submissions, certificate collection, etc.
    """

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reminders"
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    remind_at = models.DateTimeField()

    is_sent = models.BooleanField(
        default=False
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:

        ordering = [
            "remind_at"
        ]

        indexes = [

            models.Index(
                fields=[
                    "recipient",
                    "is_sent"
                ]
            ),

            models.Index(
                fields=[
                    "remind_at"
                ]
            ),

        ]

    def __str__(self):

        return f"{self.recipient.username} - {self.title}"

    @property
    def is_due(self):
        """
        Returns True when the reminder should be sent.
        """

        return (
            not self.is_sent and
            timezone.now() >= self.remind_at
        )

    @property
    def overdue(self):
        """
        Returns True if the reminder has passed and was never sent.
        """

        return (
            timezone.now() > self.remind_at and
            not self.is_sent
        )

    def mark_as_sent(self):
        """
        Marks the reminder as sent.
        """

        if not self.is_sent:

            self.is_sent = True

            self.sent_at = timezone.now()

            self.save(
                update_fields=[
                    "is_sent",
                    "sent_at"
                ]
            )

    def mark_as_read(self):
        """
        Marks the reminder as read.
        """

        if not self.is_read:

            self.is_read = True

            self.save(
                update_fields=[
                    "is_read"
                ]
            )


class Broadcast(models.Model):
    """
    Broadcast messages.

    Broadcasts are announcements sent to multiple users based on
    their role. They can be created by Super Admins or Trainers.
    """

    ROLE_CHOICES = (

        ("ALL", "All Users"),

        ("SUPER_ADMIN", "Super Admin"),

        ("TRAINER", "Trainer"),

        ("STUDENT", "Student"),

        ("FINANCE", "Finance"),

    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    target_role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default="ALL"
    )

    priority = models.CharField(
        max_length=20,
        choices=Notification.PRIORITY_CHOICES,
        default="NORMAL"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_broadcasts"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

        indexes = [

            models.Index(
                fields=[
                    "target_role"
                ]
            ),

            models.Index(
                fields=[
                    "created_at"
                ]
            ),

        ]

    def __str__(self):

        return self.title

    @property
    def total_recipients(self):
        """
        Returns the number of users that should receive
        this broadcast.
        """

        from accounts.models import User

        if self.target_role == "ALL":
            return User.objects.count()

        return User.objects.filter(
            role=self.target_role
        ).count()

    def activate(self):
        """
        Activate this broadcast.
        """

        if not self.is_active:

            self.is_active = True

            self.save(
                update_fields=[
                    "is_active"
                ]
            )

    def deactivate(self):
        """
        Deactivate this broadcast.
        """

        if self.is_active:

            self.is_active = False

            self.save(
                update_fields=[
                    "is_active"
                ]
            )
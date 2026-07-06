from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User

from assignments.models import (
    Assignment,
    AssignmentSubmission,
)

from evaluations.models import Evaluation

from certificates.models import Certificate

from lessons.models import Lesson
from logbook.models import (
    StudentLogbook,
    LogbookEntry,
)

from django.db.models.signals import pre_save, post_save

from students.models import Student


from attendance.models import (
    AttendanceSession,
    AttendanceRecord,
)

from .models import Notification


# ==========================================================
# HELPER FUNCTION
# ==========================================================

def notify_role(
    role,
    title,
    message,
    notification_type="GENERAL",
    sender=None,
    url=""
):
    """
    Send notification to all users of a specific role.
    """

    users = User.objects.filter(role=role)

    Notification.objects.bulk_create(

        [

            Notification(

                recipient=user,

                sender=sender,

                title=title,

                message=message,

                notification_type=notification_type,

                priority="NORMAL",

                url=url,

            )

            for user in users

        ]

    )


# ==========================================================
# ASSIGNMENT CREATED
# ==========================================================

@receiver(post_save, sender=Assignment)
def assignment_created(sender, instance, created, **kwargs):

    if not created:
        return

    notify_role(

        role="STUDENT",

        title="New Assignment",

        message=f"{instance.title} has been published.",

        notification_type="ASSIGNMENT",

        sender=instance.created_by,

        url="/assignments/",

    )


# ==========================================================
# ASSIGNMENT SUBMITTED
# ==========================================================

@receiver(post_save, sender=AssignmentSubmission)
def assignment_submitted(sender, instance, created, **kwargs):

    if not created:
        return

    message = (
        f"{instance.student.get_full_name() or instance.student.username} "
        f"submitted '{instance.assignment.title}'."
    )

    notify_role(

        role="TRAINER",

        title="Assignment Submitted",

        message=message,

        notification_type="SUBMISSION",

        sender=instance.student,

        url="/assignments/submissions/",

    )

    notify_role(

        role="SUPER_ADMIN",

        title="Assignment Submitted",

        message=message,

        notification_type="SUBMISSION",

        sender=instance.student,

        url="/assignments/submissions/",

    )


# ==========================================================
# ATTENDANCE SESSION CREATED
# ==========================================================

@receiver(post_save, sender=AttendanceSession)
def attendance_created(sender, instance, created, **kwargs):

    if not created:
        return

    notify_role(

        role="STUDENT",

        title="Attendance Session Open",

        message=f"Attendance for '{instance.title}' is now open.",

        notification_type="ATTENDANCE",

        sender=instance.created_by,

        url="/attendance/",

    )


# ==========================================================
# ATTENDANCE MARKED
# ==========================================================

@receiver(post_save, sender=AttendanceRecord)
def attendance_marked(sender, instance, created, **kwargs):

    if not created:
        return

    message = (
        f"{instance.student.get_full_name() or instance.student.username} "
        f"marked attendance for '{instance.session.title}'."
    )

    notify_role(

        role="TRAINER",

        title="Attendance Recorded",

        message=message,

        notification_type="ATTENDANCE",

        sender=instance.student,

        url="/attendance/report/",

    )

    notify_role(

        role="SUPER_ADMIN",

        title="Attendance Recorded",

        message=message,

        notification_type="ATTENDANCE",

        sender=instance.student,

        url="/attendance/report/",

    )

# ==========================================================
# LESSON CREATED / PUBLISHED
# ==========================================================

@receiver(post_save, sender=Lesson)
def lesson_created(sender, instance, created, **kwargs):

    # Notify only when the lesson is published
    if instance.status != "PUBLISHED":
        return

    # New published lesson
    if created:

        notify_role(

            role="STUDENT",

            title="New Lesson Available",

            message=f"{instance.title} has been published.",

            notification_type="LESSON",

            sender=instance.created_by,

            url="/lessons/",

        )

    # Draft updated to Published
    else:

        notify_role(

            role="STUDENT",

            title="Lesson Published",

            message=f"{instance.title} is now available.",

            notification_type="LESSON",

            sender=instance.created_by,

            url="/lessons/",

        )



# ==========================================================
# LOGBOOK UPLOADED
# ==========================================================

@receiver(post_save, sender=StudentLogbook)
def student_logbook_uploaded(sender, instance, created, **kwargs):

    if not created:
        return

    student_name = (
        instance.student.get_full_name()
        or instance.student.username
    )

    message = (
        f"{student_name} uploaded a new attachment logbook."
    )

    notify_role(
        role="TRAINER",
        title="New Logbook Uploaded",
        message=message,
        notification_type="LOGBOOK",
        sender=instance.student,
        url="/logbook/",
    )

    notify_role(
        role="SUPER_ADMIN",
        title="New Logbook Uploaded",
        message=message,
        notification_type="LOGBOOK",
        sender=instance.student,
        url="/logbook/",
    )

# ==========================================================
# LOGBOOK ENTRY CREATED
# ==========================================================

@receiver(post_save, sender=LogbookEntry)
def logbook_entry_created(sender, instance, created, **kwargs):

    if not created:
        return

    student_name = (
        instance.student.get_full_name()
        or instance.student.username
    )

    notify_role(
        role="TRAINER",
        title="Daily Logbook Entry",
        message=(
            f"{student_name} added a new logbook entry "
            f"for {instance.date}."
        ),
        notification_type="LOGBOOK",
        sender=instance.student,
        url="/logbook/",
    )

    notify_role(
        role="SUPER_ADMIN",
        title="Daily Logbook Entry",
        message=(
            f"{student_name} added a new logbook entry "
            f"for {instance.date}."
        ),
        notification_type="LOGBOOK",
        sender=instance.student,
        url="/logbook/",
    )


# ==========================================================
# LOGBOOK REVIEW
# ==========================================================

@receiver(post_save, sender=StudentLogbook)
def logbook_reviewed(sender, instance, created, **kwargs):

    if created:
        return

    if instance.status == "APPROVED":

        Notification.objects.create(

            recipient=instance.student,

            sender=instance.reviewed_by,

            title="Logbook Approved",

            message=(
                "Congratulations! Your attachment logbook "
                "has been approved."
            ),

            notification_type="LOGBOOK",

            priority="HIGH",

            url="/logbook/",

        )

    elif instance.status == "REJECTED":

        Notification.objects.create(

            recipient=instance.student,

            sender=instance.reviewed_by,

            title="Logbook Requires Changes",

            message=(
                "Your logbook has been returned for correction."
            ),

            notification_type="LOGBOOK",

            priority="HIGH",

            url="/logbook/",

        )

# ==========================================================
# LOGBOOK ENTRY REVIEW
# ==========================================================

@receiver(post_save, sender=LogbookEntry)
def logbook_entry_reviewed(sender, instance, created, **kwargs):

    if created:
        return

    if instance.status == "APPROVED":

        Notification.objects.create(

            recipient=instance.student,

            sender=instance.reviewed_by,

            title="Logbook Entry Approved",

            message=(
                f"Your entry '{instance.title}' has been approved."
            ),

            notification_type="LOGBOOK",

            priority="NORMAL",

            url="/logbook/",

        )

    elif instance.status == "REJECTED":

        Notification.objects.create(

            recipient=instance.student,

            sender=instance.reviewed_by,

            title="Logbook Entry Rejected",

            message=(
                f"Your entry '{instance.title}' requires revision."
            ),

            notification_type="LOGBOOK",

            priority="HIGH",

            url="/logbook/",

        )


# ==========================================================
# EVALUATION CREATED
# ==========================================================

@receiver(post_save, sender=Evaluation)
def evaluation_created(sender, instance, created, **kwargs):

    if not created:
        return

    if instance.status != "SUBMITTED":
        return

    Notification.objects.create(

        recipient=instance.student,

        sender=instance.trainer,

        title="New Evaluation Available",

        message=(
            f"Your evaluation for '{instance.lesson.title}' "
            "has been submitted."
        ),

        notification_type="GENERAL",

        priority="HIGH",

        url="/evaluations/",

    )

    notify_role(

        role="SUPER_ADMIN",

        title="Evaluation Submitted",

        message=(
            f"{instance.student.get_full_name() or instance.student.username} "
            f"has received an evaluation for '{instance.lesson.title}'."
        ),

        notification_type="GENERAL",

        sender=instance.trainer,

        url="/evaluations/",

    )

# ==========================================================
# EVALUATION STATUS UPDATED
# ==========================================================

@receiver(pre_save, sender=Evaluation)
def evaluation_pre_save(sender, instance, **kwargs):

    if not instance.pk:
        instance._old_status = None
        return

    try:
        old = Evaluation.objects.get(pk=instance.pk)
        instance._old_status = old.status

    except Evaluation.DoesNotExist:
        instance._old_status = None


@receiver(post_save, sender=Evaluation)
def evaluation_status_changed(sender, instance, created, **kwargs):

    if created:
        return

    if (
        hasattr(instance, "_old_status")
        and instance._old_status == "DRAFT"
        and instance.status == "SUBMITTED"
    ):

        Notification.objects.create(

            recipient=instance.student,

            sender=instance.trainer,

            title="Evaluation Submitted",

            message=(
                f"Your trainer has submitted your evaluation "
                f"for '{instance.lesson.title}'."
            ),

            notification_type="GENERAL",

            priority="HIGH",

            url="/evaluations/",

        )


# ==========================================================
# STORE OLD CERTIFICATE STATUS
# ==========================================================

@receiver(post_save, sender=Certificate)
def certificate_pre_save(sender, instance, **kwargs):

    if not instance.pk:
        instance._old_status = None
        return

    try:
        old = Certificate.objects.get(pk=instance.pk)
        instance._old_status = old.status

    except Certificate.DoesNotExist:
        instance._old_status = None


# ==========================================================
# CERTIFICATE ISSUED
# ==========================================================

@receiver(post_save, sender=Certificate)
def certificate_issued(sender, instance, created, **kwargs):

    should_notify = False

    if created and instance.status == "ISSUED":
        should_notify = True

    elif (
        hasattr(instance, "_old_status")
        and instance._old_status == "PENDING"
        and instance.status == "ISSUED"
    ):
        should_notify = True

    if not should_notify:
        return

    Notification.objects.create(

        recipient=instance.student,

        sender=instance.trainer,

        title="Certificate Issued",

        message=(
            f"Congratulations! Your certificate for "
            f"'{instance.course}' has been issued."
        ),

        notification_type="CERTIFICATE",

        priority="HIGH",

        url="/certificates/",

    )

    notify_role(

        role="SUPER_ADMIN",

        title="Certificate Issued",

        message=(
            f"{instance.student.get_full_name() or instance.student.username} "
            f"has been issued a certificate for '{instance.course}'."
        ),

        notification_type="CERTIFICATE",

        sender=instance.trainer,

        url="/certificates/",

    )


# ==========================================================
# CERTIFICATE REVOKED
# ==========================================================

@receiver(post_save, sender=Certificate)
def certificate_revoked(sender, instance, created, **kwargs):

    if created:
        return

    if (
        hasattr(instance, "_old_status")
        and instance._old_status != "REVOKED"
        and instance.status == "REVOKED"
    ):

        Notification.objects.create(

            recipient=instance.student,

            sender=instance.trainer,

            title="Certificate Revoked",

            message=(
                f"Your certificate for '{instance.course}' "
                "has been revoked."
            ),

            notification_type="CERTIFICATE",

            priority="URGENT",

            url="/certificates/",

        )



# ==========================================================
# STORE OLD STUDENT STATUS
# ==========================================================

@receiver(pre_save, sender=Student)
def student_pre_save(sender, instance, **kwargs):

    if not instance.pk:
        instance._old_status = None
        return

    try:
        old = Student.objects.get(pk=instance.pk)
        instance._old_status = old.status

    except Student.DoesNotExist:
        instance._old_status = None


# ==========================================================
# STORE OLD STUDENT STATUS
# ==========================================================

@receiver(pre_save, sender=Student)
def student_pre_save(sender, instance, **kwargs):

    if not instance.pk:
        instance._old_status = None
        return

    try:
        old = Student.objects.get(pk=instance.pk)
        instance._old_status = old.status

    except Student.DoesNotExist:
        instance._old_status = None

# ==========================================================
# STUDENT APPROVED
# ==========================================================

@receiver(post_save, sender=Student)
def student_approved(sender, instance, created, **kwargs):

    if created:
        return

    if (
        hasattr(instance, "_old_status")
        and instance._old_status != "APPROVED"
        and instance.status == "APPROVED"
    ):

        Notification.objects.create(

            recipient=instance.user,

            sender=instance.approved_by,

            title="Registration Approved",

            message=(
                "Congratulations! Your registration has been approved."
            ),

            notification_type="USER",

            priority="HIGH",

            url="/students/dashboard/",

        )

# ==========================================================
# STUDENT REJECTED
# ==========================================================

@receiver(post_save, sender=Student)
def student_rejected(sender, instance, created, **kwargs):

    if created:
        return

    if (
        hasattr(instance, "_old_status")
        and instance._old_status != "REJECTED"
        and instance.status == "REJECTED"
    ):

        Notification.objects.create(

            recipient=instance.user,

            sender=instance.approved_by,

            title="Registration Rejected",

            message=(
                "Your student registration was not approved. "
                "Please contact the administration."
            ),

            notification_type="USER",

            priority="URGENT",

            url="/students/profile/",

        )

# ==========================================================
# STUDENT COMPLETED
# ==========================================================

@receiver(post_save, sender=Student)
def student_completed(sender, instance, created, **kwargs):

    if created:
        return

    if (
        hasattr(instance, "_old_status")
        and instance._old_status != "COMPLETED"
        and instance.status == "COMPLETED"
    ):

        Notification.objects.create(

            recipient=instance.user,

            sender=instance.approved_by,

            title="Training Completed",

            message=(
                "Congratulations! You have successfully completed "
                "your training."
            ),

            notification_type="USER",

            priority="HIGH",

            url="/certificates/",

        )

        notify_role(

            role="TRAINER",

            title="Student Completed Training",

            message=(
                f"{instance.full_name} has completed the training programme."
            ),

            notification_type="USER",

            sender=instance.user,

            url="/students/",

        )

        notify_role(

            role="SUPER_ADMIN",

            title="Student Completed Training",

            message=(
                f"{instance.full_name} has completed the training programme."
            ),

            notification_type="USER",

            sender=instance.user,

            url="/students/",

        )
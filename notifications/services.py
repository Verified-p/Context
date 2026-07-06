# notifications/services.py

from django.contrib.auth import get_user_model
from django.db import transaction

from .models import Notification

User = get_user_model()


# ==========================================================
# INTERNAL HELPER
# ==========================================================

def _create_notifications(users, title, message, category, link=""):
    """
    Creates notifications for multiple users.
    """

    notifications = []

    for user in users:

        notifications.append(

            Notification(

                recipient=user,

                title=title,

                message=message,

                category=category,

                link=link,

            )

        )

    Notification.objects.bulk_create(notifications)


# ==========================================================
# GET USERS BY ROLE
# ==========================================================

def get_students():

    return User.objects.filter(
        role="STUDENT",
        is_active=True
    )


def get_trainers():

    return User.objects.filter(
        role="TRAINER",
        is_active=True
    )


def get_admins():

    return User.objects.filter(
        role="SUPER_ADMIN",
        is_active=True
    )


def get_trainers_and_admins():

    return User.objects.filter(
        role__in=[
            "SUPER_ADMIN",
            "TRAINER"
        ],
        is_active=True
    )


# ==========================================================
# GENERAL NOTIFICATION
# ==========================================================

@transaction.atomic
def notify_user(
    recipient,
    title,
    message,
    category="GENERAL",
    link=""
):
    """
    Notify one user.
    """

    Notification.objects.create(

        recipient=recipient,

        title=title,

        message=message,

        category=category,

        link=link,

    )


# ==========================================================
# BROADCAST
# ==========================================================

@transaction.atomic
def notify_all_students(
    title,
    message,
    category="GENERAL",
    link=""
):

    _create_notifications(

        get_students(),

        title,

        message,

        category,

        link,

    )


@transaction.atomic
def notify_all_trainers(
    title,
    message,
    category="GENERAL",
    link=""
):

    _create_notifications(

        get_trainers(),

        title,

        message,

        category,

        link,

    )


@transaction.atomic
def notify_admins(
    title,
    message,
    category="GENERAL",
    link=""
):

    _create_notifications(

        get_admins(),

        title,

        message,

        category,

        link,

    )


@transaction.atomic
def notify_trainers_and_admins(
    title,
    message,
    category="GENERAL",
    link=""
):

    _create_notifications(

        get_trainers_and_admins(),

        title,

        message,

        category,

        link,

    )


# ==========================================================
# ASSIGNMENT EVENTS
# ==========================================================

def assignment_created(assignment):

    notify_all_students(

        title="New Assignment",

        message=f"{assignment.title} has been published.",

        category="ASSIGNMENT",

        link="/assignments/",

    )


def assignment_submitted(submission):

    notify_trainers_and_admins(

        title="Assignment Submitted",

        message=(
            f"{submission.student.get_full_name() or submission.student.username} "
            f"submitted '{submission.assignment.title}'."
        ),

        category="ASSIGNMENT",

        link="/assignments/submissions/",

    )


def assignment_graded(submission):

    notify_user(

        recipient=submission.student,

        title="Assignment Graded",

        message=f"'{submission.assignment.title}' has been graded.",

        category="ASSIGNMENT",

        link="/assignments/submissions/",

    )


# ==========================================================
# LESSON EVENTS
# ==========================================================

def lesson_created(lesson):

    notify_all_students(

        title="New Lesson",

        message=f"{lesson.title} is now available.",

        category="LESSON",

        link="/lessons/",

    )


# ==========================================================
# ATTENDANCE EVENTS
# ==========================================================

def attendance_created(session):

    notify_all_students(

        title="Attendance Open",

        message=f"Attendance for '{session.title}' is now open.",

        category="ATTENDANCE",

        link="/attendance/",

    )


def attendance_marked(record):

    notify_trainers_and_admins(

        title="Attendance Submitted",

        message=(
            f"{record.student.get_full_name() or record.student.username} "
            f"marked attendance for '{record.session.title}'."
        ),

        category="ATTENDANCE",

        link="/attendance/report/",

    )


# ==========================================================
# LOGBOOK EVENTS
# ==========================================================

def logbook_submitted(entry):

    notify_trainers_and_admins(

        title="New Logbook Entry",

        message=(
            f"{entry.student.get_full_name() or entry.student.username} "
            f"submitted a new logbook entry."
        ),

        category="LOGBOOK",

        link="/logbook/",

    )


# ==========================================================
# SYSTEM EVENTS
# ==========================================================

def announcement(title, message):

    notify_all_students(

        title=title,

        message=message,

        category="ANNOUNCEMENT",

    )


def reminder(title, message):

    notify_all_students(

        title=title,

        message=message,

        category="REMINDER",

    )


def broadcast(title, message):

    users = User.objects.filter(
        is_active=True
    )

    _create_notifications(

        users,

        title,

        message,

        "BROADCAST",

        "",

    )
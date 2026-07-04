from django.contrib.auth import get_user_model
from django.db.models import Avg, Count

from attendance.models import AttendanceSession, AttendanceRecord
from assignments.models import Assignment, AssignmentSubmission

User = get_user_model()


# ==========================================================
# USER STATISTICS
# ==========================================================

def get_user_statistics():

    return {

        "total_users": User.objects.count(),

        "total_students": User.objects.filter(
            role="STUDENT"
        ).count(),

        "total_trainers": User.objects.filter(
            role="TRAINER"
        ).count(),

        "total_super_admins": User.objects.filter(
            role="SUPER_ADMIN"
        ).count(),

        "total_finance": User.objects.filter(
            role="FINANCE"
        ).count(),

        "verified_users": User.objects.filter(
            is_verified=True
        ).count(),

        "unverified_users": User.objects.filter(
            is_verified=False
        ).count(),

    }


# ==========================================================
# ATTENDANCE STATISTICS
# ==========================================================

def get_attendance_statistics():

    total_sessions = AttendanceSession.objects.count()

    active_sessions = AttendanceSession.objects.filter(
        is_active=True
    ).count()

    closed_sessions = AttendanceSession.objects.filter(
        is_active=False
    ).count()

    total_records = AttendanceRecord.objects.count()

    present = AttendanceRecord.objects.filter(
        status="PRESENT"
    ).count()

    absent = AttendanceRecord.objects.filter(
        status="ABSENT"
    ).count()

    late = AttendanceRecord.objects.filter(
        status="LATE"
    ).count()

    attendance_rate = 0

    if total_records:

        attendance_rate = round(
            (present / total_records) * 100,
            2
        )

    return {

        "total_sessions": total_sessions,

        "active_sessions": active_sessions,

        "closed_sessions": closed_sessions,

        "total_records": total_records,

        "present": present,

        "absent": absent,

        "late": late,

        "attendance_rate": attendance_rate,

    }


# ==========================================================
# ASSIGNMENT STATISTICS
# ==========================================================

def get_assignment_statistics():

    total_assignments = Assignment.objects.count()

    published = Assignment.objects.filter(
        status="PUBLISHED"
    ).count()

    drafts = Assignment.objects.filter(
        status="DRAFT"
    ).count()

    closed = Assignment.objects.filter(
        status="CLOSED"
    ).count()

    total_submissions = AssignmentSubmission.objects.count()

    graded = AssignmentSubmission.objects.filter(
        status="GRADED"
    ).count()

    pending = AssignmentSubmission.objects.filter(
        status="SUBMITTED"
    ).count()

    late_submissions = AssignmentSubmission.objects.filter(
        is_late=True
    ).count()

    average_marks = (
        AssignmentSubmission.objects.filter(
            marks_awarded__isnull=False
        ).aggregate(
            Avg("marks_awarded")
        )["marks_awarded__avg"]
        or 0
    )

    return {

        "total_assignments": total_assignments,

        "published_assignments": published,

        "draft_assignments": drafts,

        "closed_assignments": closed,

        "total_submissions": total_submissions,

        "graded_submissions": graded,

        "pending_submissions": pending,

        "late_submissions": late_submissions,

        "average_marks": round(
            average_marks,
            2
        ),

    }


# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

def get_dashboard_statistics():

    return {

        **get_user_statistics(),

        **get_attendance_statistics(),

        **get_assignment_statistics(),

    }


# ==========================================================
# RECENT ATTENDANCE
# ==========================================================

def get_recent_attendance(limit=10):

    return (
        AttendanceRecord.objects
        .select_related(
            "student",
            "session"
        )
        .order_by("-timestamp")[:limit]
    )


# ==========================================================
# RECENT SUBMISSIONS
# ==========================================================

def get_recent_submissions(limit=10):

    return (
        AssignmentSubmission.objects
        .select_related(
            "student",
            "assignment"
        )
        .order_by("-submitted_at")[:limit]
    )


# ==========================================================
# TOP STUDENTS BY ATTENDANCE
# ==========================================================

def get_top_students(limit=10):

    return (

        User.objects.filter(
            role="STUDENT"
        )

        .annotate(

            attendance_count=Count(
                "attendance_records"
            )

        )

        .order_by("-attendance_count")[:limit]

    )
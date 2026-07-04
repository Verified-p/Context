from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from attendance.models import AttendanceRecord
from assignments.models import AssignmentSubmission

from .services import (
    get_dashboard_statistics,
    get_recent_attendance,
    get_recent_submissions,
    get_top_students,
)


# ==========================================================
# HELPER
# ==========================================================

def is_staff_user(user):

    return (
        user.role in [
            "SUPER_ADMIN",
            "TRAINER",
            "FINANCE",
        ]
        or user.is_staff
    )


# ==========================================================
# REPORTS DASHBOARD
# ==========================================================

@login_required
def dashboard(request):

    context = get_dashboard_statistics()

    context["recent_attendance"] = get_recent_attendance()

    context["recent_submissions"] = get_recent_submissions()

    context["top_students"] = get_top_students()

    context["is_staff_user"] = is_staff_user(
        request.user
    )

    return render(
        request,
        "dashboard.html",
        context,
    )


# ==========================================================
# STUDENT REPORTS
# ==========================================================

@login_required
def student_reports(request):

    if is_staff_user(request.user):

        attendance = (
            AttendanceRecord.objects
            .select_related(
                "student",
                "session"
            )
            .order_by("-timestamp")
        )

        submissions = (
            AssignmentSubmission.objects
            .select_related(
                "student",
                "assignment"
            )
            .order_by("-submitted_at")
        )

    else:

        attendance = (
            AttendanceRecord.objects
            .filter(student=request.user)
            .select_related("session")
            .order_by("-timestamp")
        )

        submissions = (
            AssignmentSubmission.objects
            .filter(student=request.user)
            .select_related("assignment")
            .order_by("-submitted_at")
        )

    context = {

        "attendance_records": attendance,

        "assignment_submissions": submissions,

        "attendance_count": attendance.count(),

        "submission_count": submissions.count(),

        "is_staff_user": is_staff_user(
            request.user
        ),

    }

    return render(
        request,
        "student_reports.html",
        context,
    )


# ==========================================================
# ATTENDANCE REPORTS
# ==========================================================

@login_required
def attendance_reports(request):

    if is_staff_user(request.user):

        records = (
            AttendanceRecord.objects
            .select_related(
                "student",
                "session"
            )
            .order_by("-timestamp")
        )

    else:

        records = (
            AttendanceRecord.objects
            .filter(student=request.user)
            .select_related("session")
            .order_by("-timestamp")
        )

    context = {

        "records": records,

        "total": records.count(),

        "present": records.filter(
            status="PRESENT"
        ).count(),

        "late": records.filter(
            status="LATE"
        ).count(),

        "absent": records.filter(
            status="ABSENT"
        ).count(),

        "is_staff_user": is_staff_user(
            request.user
        ),

    }

    return render(
        request,
        "attendance_reports.html",
        context,
    )


# ==========================================================
# ASSIGNMENT REPORTS
# ==========================================================

@login_required
def assignment_reports(request):

    if is_staff_user(request.user):

        submissions = (
            AssignmentSubmission.objects
            .select_related(
                "student",
                "assignment"
            )
            .order_by("-submitted_at")
        )

    else:

        submissions = (
            AssignmentSubmission.objects
            .filter(student=request.user)
            .select_related("assignment")
            .order_by("-submitted_at")
        )

    context = {

        "submissions": submissions,

        "total": submissions.count(),

        "graded": submissions.filter(
            status="GRADED"
        ).count(),

        "pending": submissions.filter(
            status="SUBMITTED"
        ).count(),

        "late": submissions.filter(
            is_late=True
        ).count(),

        "is_staff_user": is_staff_user(
            request.user
        ),

    }

    return render(
        request,
        "assignment_reports.html",
        context,
    )


# ==========================================================
# FINANCE REPORTS
# ==========================================================

@login_required
def finance_reports(request):

    return render(
        request,
        "finance_reports.html",
        {
            "coming_soon": True,
        },
    )


# ==========================================================
# ANALYTICS
# ==========================================================

@login_required
def analytics(request):

    context = get_dashboard_statistics()

    context["top_students"] = get_top_students()

    return render(
        request,
        "analytics.html",
        context,
    )
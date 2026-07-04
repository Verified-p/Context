from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from accounts.models import User
from attendance.models import AttendanceSession, AttendanceRecord
from assignments.models import Assignment, AssignmentSubmission

from .services import get_dashboard_url


# ==========================================
# ROUTER VIEW
# ==========================================

@login_required
def dashboard_router(request):

    return redirect(
        get_dashboard_url(request.user)
    )


# ==========================================
# SUPER ADMIN DASHBOARD
# ==========================================

@login_required
def admin_dashboard(request):

    if request.user.role != "SUPER_ADMIN":
        return redirect("dashboard:router")

    now = timezone.now()

    context = {

        "total_users": User.objects.count(),

        "total_students": User.objects.filter(
            role="STUDENT"
        ).count(),

        "total_trainers": User.objects.filter(
            role="TRAINER"
        ).count(),

        "verified_users": User.objects.filter(
            is_verified=True
        ).count(),

        "active_attendance": AttendanceSession.objects.filter(
            is_active=True,
            expires_at__gte=now
        ).count(),

        "attendance_records": AttendanceRecord.objects.count(),

        "assignments": Assignment.objects.count(),

        "submissions": AssignmentSubmission.objects.count(),

        "recent_users": User.objects.order_by(
            "-date_joined"
        )[:5],

    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )


# ==========================================
# TRAINER DASHBOARD
# ==========================================

@login_required
def trainer_dashboard(request):

    if request.user.role != "TRAINER":
        return redirect("dashboard:router")

    now = timezone.now()

    my_assignments = Assignment.objects.filter(
        created_by=request.user
    )

    my_sessions = AttendanceSession.objects.filter(
        created_by=request.user
    )

    context = {

        "my_assignments": my_assignments.count(),

        "published_assignments": my_assignments.filter(
            status="PUBLISHED"
        ).count(),

        "active_sessions": my_sessions.filter(
            is_active=True,
            expires_at__gte=now
        ).count(),

        "attendance_records": AttendanceRecord.objects.filter(
            session__created_by=request.user
        ).count(),

        "pending_grading": AssignmentSubmission.objects.filter(
            assignment__created_by=request.user,
            status="SUBMITTED"
        ).count(),

        "recent_submissions": AssignmentSubmission.objects.filter(
            assignment__created_by=request.user
        ).select_related(
            "student",
            "assignment"
        ).order_by("-submitted_at")[:5],

    }

    return render(
        request,
        "trainer_dashboard.html",
        context
    )


# ==========================================
# STUDENT DASHBOARD
# ==========================================

@login_required
def student_dashboard(request):

    if request.user.role != "STUDENT":
        return redirect("dashboard:router")

    now = timezone.now()

    attendance_records = AttendanceRecord.objects.filter(
        student=request.user
    )

    total = attendance_records.count()

    present = attendance_records.filter(
        status="PRESENT"
    ).count()

    if total > 0:
        attendance_percentage = round(
            (present / total) * 100,
            1
        )
    else:
        attendance_percentage = 0

    active_session = AttendanceSession.objects.filter(
        is_active=True,
        opens_at__lte=now,
        expires_at__gte=now
    ).first()

    assignments = Assignment.objects.filter(
        status="PUBLISHED"
    )

    submissions = AssignmentSubmission.objects.filter(
        student=request.user
    )

    context = {

        "attendance_percentage": attendance_percentage,

        "attendance_records": total,

        "active_session": active_session,

        "assignments": assignments.count(),

        "submitted": submissions.count(),

        "pending": assignments.count() - submissions.count(),

        "recent_assignments": assignments.order_by(
            "due_date"
        )[:5],

        "recent_submissions": submissions.order_by(
            "-submitted_at"
        )[:5],

    }

    return render(
        request,
        "student_dashboard.html",
        context
    )


# ==========================================
# FINANCE DASHBOARD
# ==========================================

@login_required
def finance_dashboard(request):

    if request.user.role != "FINANCE":
        return redirect("dashboard:router")

    context = {

        "students": User.objects.filter(
            role="STUDENT"
        ).count(),

        "verified_students": User.objects.filter(
            role="STUDENT",
            is_verified=True
        ).count(),

    }

    return render(
        request,
        "finance_dashboard.html",
        context
    )
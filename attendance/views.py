from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import AttendanceSession, AttendanceRecord
from .forms import AttendanceSessionForm

from .qr.generator import generate_qr
from .qr.utils import build_qr_payload
from .qr.scanner import mark_attendance

from django.db.models import Q

# ==========================================================
# HELPER
# ==========================================================

def is_trainer_or_admin(user):
    """
    Returns True if the logged-in user is an admin or trainer.
    """

    return (
        user.is_staff or
        getattr(user, "role", "").upper() == "TRAINER"
    )
# ==========================================================
# ATTENDANCE DASHBOARD
# ==========================================================
@login_required
def attendance_dashboard(request):

    now = timezone.now()

    # Automatically close expired attendance sessions
    AttendanceSession.objects.filter(
        is_active=True,
        expires_at__lt=now
    ).update(is_active=False)

    if is_trainer_or_admin(request.user):

        # Trainers/Admins see every session
        sessions = (
            AttendanceSession.objects
            .select_related("created_by")
            .order_by("-created_at")
        )

    else:

        # Students see every active session
        sessions = (
            AttendanceSession.objects
            .filter(is_active=True)
            .select_related("created_by")
            .order_by("-created_at")
        )

    context = {

        "sessions": sessions,

        "total_sessions": AttendanceSession.objects.count(),

        "total_records": AttendanceRecord.objects.count(),

        "active_sessions": AttendanceSession.objects.filter(
            is_active=True
        ).count(),

        "is_trainer": is_trainer_or_admin(request.user),

        "now": now,

    }

    return render(
        request,
        "attendance_dashboard.html",
        context
    )

# ==========================================================
# CREATE ATTENDANCE SESSION
# ==========================================================
# ==========================================================
# CREATE ATTENDANCE SESSION
# ==========================================================
@login_required
def create_session(request):

    # Only trainers/admins can create attendance
    if not is_trainer_or_admin(request.user):

        messages.error(
            request,
            "Only trainers or administrators can create attendance sessions."
        )

        return redirect("attendance:dashboard")

    if request.method == "POST":

        form = AttendanceSessionForm(request.POST)

        if form.is_valid():

            session = form.save(commit=False)

            # Assign creator
            session.created_by = request.user

            # Open attendance immediately
            session.opens_at = timezone.now()

            # Ensure it is active
            session.is_active = True

            # Let the model calculate expires_at from duration_minutes
            session.expires_at = None

            # Save session
            session.save()

            messages.success(
                request,
                f"Attendance session '{session.title}' has been created successfully. Students can now mark attendance."
            )

            return redirect(
                "attendance:session_detail",
                session.pk
            )

    else:

        form = AttendanceSessionForm()

    return render(
        request,
        "create_session.html",
        {
            "form": form,
        }
    )


# ==========================================================
# ATTENDANCE SESSION DETAILS
# ==========================================================
@login_required
def session_detail(request, pk):

    session = get_object_or_404(
        AttendanceSession.objects.select_related("created_by"),
        pk=pk
    )

    if session.is_expired and session.is_active:

        session.is_active = False
        session.save(update_fields=["is_active"])

    if (
        not is_trainer_or_admin(request.user)
        and not session.is_open
    ):

        messages.error(
            request,
            "This attendance session is no longer available."
        )

        return redirect("attendance:dashboard")

    qr_data = build_qr_payload(session.session_token)

    qr_code = generate_qr(qr_data)

    records = (
        session.records
        .select_related("student")
        .order_by("-timestamp")
    )

    context = {

        "session": session,

        "records": records,

        "qr_code": qr_code,

        "time_remaining": session.time_remaining,

        "is_open": session.is_open,

        "is_trainer": is_trainer_or_admin(request.user),

        "now": timezone.now(),

    }

    return render(
        request,
        "attendance_list.html",
        context
    )


# ==========================================================
# STUDENT QR SCAN / MARK ATTENDANCE
# ==========================================================
# ==========================================================
# STUDENT QR SCAN / MARK ATTENDANCE
# ==========================================================
@login_required
def scan_qr(request, token):

    now = timezone.now()

    session = get_object_or_404(
        AttendanceSession,
        session_token=token
    )

    # Automatically close expired sessions
    if session.is_active and session.expires_at <= now:

        session.is_active = False
        session.save(update_fields=["is_active"])

    # Session has not opened yet
    if now < session.opens_at:

        messages.warning(
            request,
            "This attendance session has not started yet."
        )

        return redirect("attendance:dashboard")

    # Session has already closed
    if not session.is_open:

        messages.error(
            request,
            "This attendance session has already closed."
        )

        return redirect("attendance:dashboard")

    # Record attendance
    result = mark_attendance(
        token,
        request.user
    )

    if result["status"] == "success":

        messages.success(
            request,
            result["message"]
        )

    elif result["status"] == "warning":

        messages.warning(
            request,
            result["message"]
        )

    else:

        messages.error(
            request,
            result["message"]
        )

    # Redirect to the attendance report view,
    # which loads the records correctly.
    return redirect("attendance:report")

# ==========================================================
# ATTENDANCE REPORT
# ==========================================================
@login_required
def attendance_report(request):

    if is_trainer_or_admin(request.user):

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

        "total_records": records.count(),

        "present_count": records.filter(
            status="PRESENT"
        ).count(),

        "late_count": records.filter(
            status="LATE"
        ).count(),

        "absent_count": records.filter(
            status="ABSENT"
        ).count(),

        "sessions_covered": (
            records.values("session")
            .distinct()
            .count()
        ),

        "is_trainer": is_trainer_or_admin(request.user),

        "now": timezone.now(),

    }

    return render(
        request,
        "attendance_report.html",
        context
    )

# ==========================================================
# ATTENDANCE STATISTICS
# ==========================================================
@login_required
def attendance_stats(request):

    if not is_trainer_or_admin(request.user):

        messages.error(
            request,
            "You are not authorized to view attendance statistics."
        )

        return redirect("attendance:dashboard")

    total_sessions = AttendanceSession.objects.count()

    active_sessions = AttendanceSession.objects.filter(
        is_active=True
    ).count()

    closed_sessions = AttendanceSession.objects.filter(
        is_active=False
    ).count()

    total_records = AttendanceRecord.objects.count()

    present_count = AttendanceRecord.objects.filter(
        status="PRESENT"
    ).count()

    late_count = AttendanceRecord.objects.filter(
        status="LATE"
    ).count()

    absent_count = AttendanceRecord.objects.filter(
        status="ABSENT"
    ).count()

    attendance_percentage = 0

    if total_records > 0:

        attendance_percentage = round(
            (present_count / total_records) * 100,
            1
        )

    context = {

        "total_sessions": total_sessions,

        "active_sessions": active_sessions,

        "closed_sessions": closed_sessions,

        "total_records": total_records,

        "present_count": present_count,

        "late_count": late_count,

        "absent_count": absent_count,

        "attendance_percentage": attendance_percentage,

        "is_trainer": True,

        "now": timezone.now(),

    }

    return render(
        request,
        "attendance_stats.html",
        context
    )
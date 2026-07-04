from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from certificates.models import Certificate

from assignments.models import Assignment
from attendance.models import AttendanceSession, AttendanceRecord
from students.models import Student

from django.contrib.auth.decorators import login_required


from students.models import Student
from evaluations.models import Evaluation
from logbook.models import LogbookEntry

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from students.models import Student
from certificates.services import CertificateService


# =========================
# TRAINER DASHBOARD
# =========================


@login_required
def trainer_dashboard(request):

    if request.user.role not in ["TRAINER", "SUPER_ADMIN"]:
        return render(request, "403.html")

    # =========================
    # TRAINER-OWNED DATA
    # =========================
    assignments = Assignment.objects.filter(created_by=request.user)
    sessions = AttendanceSession.objects.filter(created_by=request.user)
    evaluations = Evaluation.objects.filter(trainer=request.user)

    # Logbook entries reviewed by trainer
    logbook_reviews = LogbookEntry.objects.filter(reviewed_by=request.user)

    # Students (optional: system-wide or filtered later by course)
    total_students = Student.objects.count()

    # =========================
    # COUNTS (DASHBOARD METRICS)
    # =========================
    total_assignments = assignments.count()
    published_assignments = assignments.filter(status="PUBLISHED").count()

    total_sessions = sessions.count()
    total_evaluations = evaluations.count()
    total_log_reviews = logbook_reviews.count()

    # =========================
    # RECENT ACTIVITY (IMPORTANT UPGRADE)
    # =========================
    recent_assignments = assignments.order_by("-created_at")[:5]
    recent_evaluations = evaluations.order_by("-created_at")[:5]
    recent_logs = logbook_reviews.order_by("-created_at")[:5]

    context = {
        # stats
        "total_assignments": total_assignments,
        "published_assignments": published_assignments,
        "total_sessions": total_sessions,
        "total_students": total_students,
        "total_evaluations": total_evaluations,
        "total_log_reviews": total_log_reviews,

        # activity feeds
        "recent_assignments": recent_assignments,
        "recent_evaluations": recent_evaluations,
        "recent_logs": recent_logs,
    }

    return render(request, "trainer_dashboard.html", context)


# =========================
# TRAINER STUDENTS VIEW
# =========================
@login_required
def trainer_students(request):

    students = Student.objects.select_related("user").all()

    return render(request, "trainer_students.html", {
        "students": students
    })


# =========================
# TRAINER LIST ASSIGNMENTS
# =========================
@login_required
def trainer_assignments(request):

    assignments = Assignment.objects.all()

    return render(request, "trainer_list.html", {
        "assignments": assignments
    })


# =========================
# TRAINER PROFILE
# =========================
@login_required
def trainer_profile(request):

    return render(request, "trainer_profile.html")




@login_required
def generate_certificate(request, student_id):

    if request.user.role not in ["TRAINER", "SUPER_ADMIN"]:
        return render(request, "403.html")

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if student.status != "APPROVED":

        messages.error(
            request,
            "Student must be approved before certificate generation."
        )

        return redirect("trainers:students")

    existing = Certificate.objects.filter(
        student=student.user,
        course=student.course
    ).first()

    if existing:

        messages.warning(
            request,
            "Certificate already exists."
        )

        return redirect(
            "certificates:detail",
            pk=existing.id
        )

    certificate = CertificateService.issue_certificate(
        student=student.user,
        trainer=request.user,
        course=student.course
    )

    messages.success(
        request,
        f"Certificate generated successfully for {student.full_name}."
    )

    return redirect(
        "certificates:detail",
        pk=certificate.id
    )
from django.utils import timezone
from datetime import timedelta

from .models import AttendanceSession
from .models import AttendanceRecord


# ==========================================
# CREATE ATTENDANCE SESSION
# ==========================================

def create_attendance_session(
    title,
    course,
    created_by,
    duration_minutes=30
):
    """
    Create a new attendance session.
    """

    expires_at = timezone.now() + timedelta(
        minutes=duration_minutes
    )

    return AttendanceSession.objects.create(
        title=title,
        course=course,
        created_by=created_by,
        expires_at=expires_at,
        is_active=True
    )


# ==========================================
# CLOSE ATTENDANCE SESSION
# ==========================================

def close_attendance_session(session):
    """
    Disable attendance session.
    """

    session.is_active = False
    session.save()

    return session


# ==========================================
# MARK ATTENDANCE
# ==========================================

def mark_student_attendance(
    session,
    student,
    status="PRESENT"
):
    """
    Record attendance once only.
    """

    record, created = AttendanceRecord.objects.get_or_create(
        session=session,
        student=student,
        defaults={
            "status": status
        }
    )

    return record, created


# ==========================================
# GET SESSION ATTENDANCE COUNT
# ==========================================

def get_attendance_count(session):
    """
    Return total students present.
    """

    return AttendanceRecord.objects.filter(
        session=session
    ).count()


# ==========================================
# GET ATTENDANCE STATISTICS
# ==========================================

def attendance_statistics():

    return {
        "sessions": AttendanceSession.objects.count(),
        "records": AttendanceRecord.objects.count(),
        "present": AttendanceRecord.objects.filter(
            status="PRESENT"
        ).count(),
        "late": AttendanceRecord.objects.filter(
            status="LATE"
        ).count(),
        "absent": AttendanceRecord.objects.filter(
            status="ABSENT"
        ).count(),
    }
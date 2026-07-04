from django.utils import timezone

from ..models import AttendanceSession
from ..models import AttendanceRecord


def mark_attendance(session_token, student):
    """
    Marks attendance for a student.
    Returns a dictionary describing the result.
    """

    try:

        session = AttendanceSession.objects.get(
            session_token=session_token,
            is_active=True
        )

    except AttendanceSession.DoesNotExist:

        return {
            "status": "error",
            "message": "Attendance session not found or has already closed."
        }

    # Session expired
    if session.expires_at and timezone.now() >= session.expires_at:

        session.is_active = False
        session.save(update_fields=["is_active"])

        return {
            "status": "error",
            "message": "This attendance session has expired."
        }

    # Prevent duplicate attendance
    attendance, created = AttendanceRecord.objects.get_or_create(
        session=session,
        student=student,
        defaults={
            "status": "PRESENT"
        }
    )

    if not created:

        return {
            "status": "warning",
            "message": "You have already marked attendance for this session.",
            "session": session.title
        }

    return {
        "status": "success",
        "message": "Attendance recorded successfully.",
        "session": session.title,
        "record": attendance
    }
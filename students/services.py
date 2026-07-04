from django.utils import timezone


def approve_student(student, approved_by=None):
    """
    Approve a student.
    """

    student.status = "APPROVED"
    student.approved_by = approved_by
    student.approved_at = timezone.now()

    student.save()

    return student


def reject_student(student):
    """
    Reject a student.
    """

    student.status = "REJECTED"
    student.save()

    return student
from django.utils import timezone

from .models import (
    Assignment,
    AssignmentSubmission
)


def publish_assignment(assignment):
    """
    Publish assignment
    """

    assignment.status = "PUBLISHED"
    assignment.save()

    return assignment


def close_assignment(assignment):
    """
    Close assignment
    """

    assignment.status = "CLOSED"
    assignment.save()

    return assignment


def grade_submission(
    submission,
    marks,
    feedback,
    grader
):
    """
    Grade student submission
    """

    submission.marks_awarded = marks
    submission.feedback = feedback
    submission.graded_by = grader
    submission.graded_at = timezone.now()
    submission.status = "GRADED"

    submission.save()

    return submission


def assignment_statistics(assignment):
    """
    Assignment statistics
    """

    submissions = assignment.submissions.all()

    total_submissions = submissions.count()

    graded_submissions = submissions.filter(
        status="GRADED"
    ).count()

    late_submissions = submissions.filter(
        is_late=True
    ).count()

    average_score = 0

    graded = submissions.filter(
        marks_awarded__isnull=False
    )

    if graded.exists():

        total_marks = sum(
            float(item.marks_awarded)
            for item in graded
        )

        average_score = round(
            total_marks / graded.count(),
            2
        )

    return {
        "total_submissions": total_submissions,
        "graded_submissions": graded_submissions,
        "late_submissions": late_submissions,
        "average_score": average_score
    }


def student_assignment_summary(student):
    """
    Student assignment dashboard statistics
    """

    submissions = AssignmentSubmission.objects.filter(
        student=student
    )

    total = submissions.count()

    graded = submissions.filter(
        status="GRADED"
    ).count()

    pending = submissions.filter(
        status="SUBMITTED"
    ).count()

    late = submissions.filter(
        is_late=True
    ).count()

    return {
        "total": total,
        "graded": graded,
        "pending": pending,
        "late": late
    }
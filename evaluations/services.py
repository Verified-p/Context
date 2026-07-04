from django.db.models import Avg, Count

from .models import Evaluation
from attendance.models import AttendanceRecord
from assignments.models import AssignmentSubmission
from logbook.models import LogbookEntry


# =========================
# BASIC EVALUATION ANALYTICS
# =========================

def calculate_student_average(student):
    evaluations = Evaluation.objects.filter(student=student)

    if not evaluations.exists():
        return 0

    return round(
        evaluations.aggregate(avg=Avg("total_score"))["avg"] or 0,
        2
    )


def get_lesson_performance(student, lesson):
    evaluation = Evaluation.objects.filter(
        student=student,
        lesson=lesson
    ).order_by("-created_at").first()

    return evaluation.total_score if evaluation else 0


def get_course_performance(lesson):
    evaluations = Evaluation.objects.filter(lesson=lesson)

    if not evaluations.exists():
        return {"avg": 0, "count": 0}

    return {
        "avg": round(evaluations.aggregate(avg=Avg("total_score"))["avg"] or 0, 2),
        "count": evaluations.count()
    }


# =========================
# STUDENT ANALYTICS CORE
# =========================

def get_student_analytics(student):

    evaluations = Evaluation.objects.filter(student=student)

    if not evaluations.exists():
        return {
            "average": 0,
            "highest": 0,
            "lowest": 0,
            "total": 0,
        }

    scores = list(evaluations.values_list("total_score", flat=True))

    return {
        "average": round(sum(scores) / len(scores), 2),
        "highest": max(scores),
        "lowest": min(scores),
        "total": len(scores),
    }


# =========================
# TREND ANALYTICS
# =========================

def get_evaluation_trends(student):

    evaluations = Evaluation.objects.filter(student=student).order_by("created_at")

    return {
        "labels": [e.lesson.title for e in evaluations],
        "scores": [e.total_score for e in evaluations],
    }


# =========================
# TOP & WEAK STUDENTS
# =========================

def get_top_students(limit=10):

    return (
        Evaluation.objects
        .values("student__id", "student__username")
        .annotate(avg_score=Avg("total_score"))
        .order_by("-avg_score")[:limit]
    )


def get_weak_students(limit=10):

    return (
        Evaluation.objects
        .values("student__id", "student__username")
        .annotate(avg_score=Avg("total_score"))
        .order_by("avg_score")[:limit]
    )


# =========================
# ATTENDANCE + PERFORMANCE
# =========================

def attendance_performance_summary(student):

    attendance_records = AttendanceRecord.objects.filter(student=student)

    total_attendance = attendance_records.count()
    present = attendance_records.filter(status="PRESENT").count()

    attendance_rate = (
        round((present / total_attendance) * 100, 2)
        if total_attendance > 0 else 0
    )

    evaluations = Evaluation.objects.filter(student=student)

    avg_score = (
        round(evaluations.aggregate(avg=Avg("total_score"))["avg"] or 0, 2)
        if evaluations.exists() else 0
    )

    return {
        "attendance_rate": attendance_rate,
        "total_sessions": total_attendance,
        "average_score": avg_score,
    }


# =========================
# LOGBOOK INTEGRATION (NEW)
# =========================

def logbook_quality_score(student):

    logs = LogbookEntry.objects.filter(student=student)

    if not logs.exists():
        return 0

    return round(logs.aggregate(avg=Avg("score"))["avg"] or 0, 2)


# =========================
# FINAL LMS PERFORMANCE INDEX
# =========================

def get_student_overall_index(student):

    eval_avg = calculate_student_average(student)
    log_score = logbook_quality_score(student)
    attendance = attendance_performance_summary(student)["attendance_rate"]

    # weighted LMS score
    final = (
        (eval_avg * 0.45) +
        (log_score * 0.25) +
        (attendance * 0.30)
    )

    return round(final, 2)

class EvaluationAnalyticsService:
    """
    Wrapper class for analytics (clean API for views)
    """

    @staticmethod
    def student_average(student):
        return calculate_student_average(student)

    @staticmethod
    def lesson_performance(student, lesson):
        return get_lesson_performance(student, lesson)

    @staticmethod
    def trends(student):
        return get_evaluation_trends(student)

    @staticmethod
    def top_students(limit=10):
        return get_top_students(limit)

    @staticmethod
    def weak_students(limit=10):
        return get_weak_students(limit)

    @staticmethod
    def attendance_vs_performance(student):
        return attendance_performance_summary(student)

    @staticmethod
    def overall_index(student):
        return get_student_overall_index(student)
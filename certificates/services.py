from django.db.models import Avg

from assignments.models import AssignmentSubmission
from attendance.models import AttendanceRecord
from evaluations.models import Evaluation
from logbook.models import LogbookEntry

from .models import Certificate, CertificateRequirement

from .pdf.certificate_generator import CertificatePDFGenerator
from .pdf.recommendation_generator import RecommendationPDFGenerator


# ==========================================
# DEVELOPMENT MODE
# ==========================================
# Set to False when the system goes live
# and all student records are available.
# ==========================================

TEST_MODE = True


class CertificateService:

    # =====================================
    # ATTENDANCE SCORE
    # =====================================

    @staticmethod
    def calculate_attendance(student):

        records = AttendanceRecord.objects.filter(
            student=student
        )

        if not records.exists():
            return 0

        present = records.filter(
            status="PRESENT"
        ).count()

        return round(
            (present / records.count()) * 100,
            2
        )

    # =====================================
    # ASSIGNMENT SCORE
    # =====================================

    @staticmethod
    def calculate_assignments(student):

        submissions = (
            AssignmentSubmission.objects
            .filter(student=student)
            .exclude(marks_awarded__isnull=True)
        )

        if not submissions.exists():
            return 0

        scores = []

        for submission in submissions:

            if hasattr(submission, "percentage_score"):
                scores.append(
                    submission.percentage_score
                )

        if not scores:
            return 0

        return round(
            sum(scores) / len(scores),
            2
        )

    # =====================================
    # EVALUATION SCORE
    # =====================================

    @staticmethod
    def calculate_evaluations(student):

        evaluations = Evaluation.objects.filter(
            student=student
        )

        if not evaluations.exists():
            return 0

        return round(
            evaluations.aggregate(
                avg=Avg("total_score")
            )["avg"] or 0,
            2
        )

    # =====================================
    # LOGBOOK SCORE
    # =====================================

    @staticmethod
    def calculate_logbook(student):

        logs = LogbookEntry.objects.filter(
            student=student
        )

        if not logs.exists():
            return 0

        return round(
            logs.aggregate(
                avg=Avg("score")
            )["avg"] or 0,
            2
        )

    # =====================================
    # ELIGIBILITY CHECK
    # =====================================

    @staticmethod
    def is_eligible(student, course):

        attendance = (
            CertificateService.calculate_attendance(
                student
            )
        )

        evaluation = (
            CertificateService.calculate_evaluations(
                student
            )
        )

        assignment = (
            CertificateService.calculate_assignments(
                student
            )
        )

        logbook = (
            CertificateService.calculate_logbook(
                student
            )
        )

        try:

            req = CertificateRequirement.objects.get(
                course=course
            )

            eligible = (
                attendance >= req.min_attendance and
                evaluation >= req.min_evaluation and
                assignment >= req.min_assignment and
                logbook >= req.min_logbook
            )

        except CertificateRequirement.DoesNotExist:

            eligible = TEST_MODE

        return {
            "eligible": eligible,
            "attendance": attendance,
            "evaluation": evaluation,
            "assignment": assignment,
            "logbook": logbook,
        }

    # =====================================
    # ISSUE CERTIFICATE
    # =====================================

    @staticmethod
    def issue_certificate(
        student,
        trainer,
        course
    ):

        existing = Certificate.objects.filter(
            student=student,
            course=course
        ).first()

        if existing:
            return existing

        result = CertificateService.is_eligible(
            student,
            course
        )

        # =================================
        # STRICT CHECK DISABLED IN TEST MODE
        # =================================

        if not result["eligible"] and not TEST_MODE:

            raise ValueError(
                "Student does not meet certificate requirements."
            )

        certificate = Certificate.objects.create(
            student=student,
            trainer=trainer,
            course=course,
            attendance_score=result.get(
                "attendance",
                0
            ),
            evaluation_score=result.get(
                "evaluation",
                0
            ),
            assignment_score=result.get(
                "assignment",
                0
            ),
            logbook_score=result.get(
                "logbook",
                0
            ),
        )

        return certificate

    # =====================================
    # CERTIFICATE SUMMARY
    # =====================================

    @staticmethod
    def certificate_summary(student):

        certificates = Certificate.objects.filter(
            student=student
        )

        return {
            "total": certificates.count(),
            "issued": certificates.filter(
                status="ISSUED"
            ).count(),
            "pending": certificates.filter(
                status="PENDING"
            ).count(),
            "revoked": certificates.filter(
                status="REVOKED"
            ).count(),
        }


# ==========================================
# PDF SERVICES
# ==========================================

class CertificatePDFService:

    @staticmethod
    def generate_certificate_pdf(
        certificate
    ):

        generator = CertificatePDFGenerator(
            certificate
        )

        return generator.generate()

    @staticmethod
    def generate_recommendation_pdf(certificate):

        generator = RecommendationPDFGenerator(
        certificate
    )

        return generator.generate()
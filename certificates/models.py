from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Certificate(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("ISSUED", "Issued"),
        ("REVOKED", "Revoked"),
    )

    GRADE_CHOICES = (
        ("DISTINCTION", "Distinction"),
        ("CREDIT", "Credit"),
        ("PASS", "Pass"),
        ("FAIL", "Fail"),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="certificates"
    )

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issued_certificates"
    )

    course = models.CharField(
        max_length=255
    )

    certificate_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )

    attendance_score = models.FloatField(
        default=0
    )

    evaluation_score = models.FloatField(
        default=0
    )

    assignment_score = models.FloatField(
        default=0
    )

    logbook_score = models.FloatField(
        default=0
    )

    final_score = models.FloatField(
        default=0
    )

    grade = models.CharField(
        max_length=20,
        choices=GRADE_CHOICES,
        default="FAIL"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    completion_date = models.DateField(
        null=True,
        blank=True
    )

    issued_at = models.DateTimeField(
        null=True,
        blank=True
    )

    verification_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    revoked_reason = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.certificate_number} - {self.student.username}"

    def calculate_final_score(self):

        return round(
            (
                self.attendance_score * 0.25 +
                self.evaluation_score * 0.30 +
                self.assignment_score * 0.25 +
                self.logbook_score * 0.20
            ),
            2
        )

    def calculate_grade(self):

        score = self.final_score

        if score >= 80:
            return "DISTINCTION"

        elif score >= 70:
            return "CREDIT"

        elif score >= 50:
            return "PASS"

        return "FAIL"

    def generate_certificate_number(self):

        if self.certificate_number:
            return

        year = timezone.now().year

        last_certificate = (
            Certificate.objects
            .filter(created_at__year=year)
            .order_by("-id")
            .first()
        )

        if last_certificate:

            try:
                last_number = int(
                    last_certificate.certificate_number.split("-")[-1]
                )

            except Exception:
                last_number = 0

        else:
            last_number = 0

        next_number = last_number + 1

        self.certificate_number = (
            f"CETMS-{year}-{str(next_number).zfill(6)}"
        )

    @property
    def is_valid(self):
        return self.status == "ISSUED"

    def save(self, *args, **kwargs):

        if not self.certificate_number:
            self.generate_certificate_number()

        self.final_score = self.calculate_final_score()

        self.grade = self.calculate_grade()

        # ============================
        # ISSUED CERTIFICATES
        # ============================

        if self.status == "ISSUED":

            if not self.issued_at:
                self.issued_at = timezone.now()

            if not self.completion_date:
                self.completion_date = timezone.now().date()

        # ============================
        # AUTO ISSUE IF SCORE >= 50
        # ============================

        elif (
            self.status == "PENDING"
            and self.final_score >= 50
        ):

            self.status = "ISSUED"

            if not self.issued_at:
                self.issued_at = timezone.now()

            if not self.completion_date:
                self.completion_date = timezone.now().date()

        # ============================
        # DEFAULT REMARKS
        # ============================

        if not self.remarks:

            if self.status == "ISSUED":

                if self.grade == "DISTINCTION":

                    self.remarks = (
                        "Excellent performance. Certificate awarded."
                    )

                elif self.grade == "CREDIT":

                    self.remarks = (
                        "Very good performance. Certificate awarded."
                    )

                elif self.grade == "PASS":

                    self.remarks = (
                        "Successfully completed the course."
                    )

                else:

                    self.remarks = (
                        "Certificate manually approved."
                    )

            elif self.status == "REVOKED":

                self.remarks = (
                    self.revoked_reason
                    or
                    "Certificate has been revoked."
                )

            else:

                self.remarks = (
                    "Awaiting certificate approval."
                )

        super().save(*args, **kwargs)


class CertificateRequirement(models.Model):

    course = models.CharField(
        max_length=255,
        unique=True
    )

    min_attendance = models.FloatField(
        default=75
    )

    min_evaluation = models.FloatField(
        default=60
    )

    min_assignment = models.FloatField(
        default=60
    )

    min_logbook = models.FloatField(
        default=60
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.course
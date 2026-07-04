from django.contrib import admin
from django.utils import timezone

from .models import Certificate, CertificateRequirement


# ==================================================
# CERTIFICATE ADMIN ACTIONS
# ==================================================

@admin.action(description="Issue selected certificates")
def issue_certificates(modeladmin, request, queryset):

    updated = 0

    for certificate in queryset:

        if certificate.status != "ISSUED":

            certificate.status = "ISSUED"

            if not certificate.issued_at:
                certificate.issued_at = timezone.now()

            if not certificate.completion_date:
                certificate.completion_date = timezone.now().date()

            certificate.save()

            updated += 1

    modeladmin.message_user(
        request,
        f"{updated} certificate(s) successfully issued."
    )


@admin.action(description="Revoke selected certificates")
def revoke_certificates(modeladmin, request, queryset):

    updated = queryset.update(
        status="REVOKED",
        revoked_reason="Revoked by administrator."
    )

    modeladmin.message_user(
        request,
        f"{updated} certificate(s) successfully revoked."
    )


@admin.action(description="Restore selected certificates")
def restore_certificates(modeladmin, request, queryset):

    updated = 0

    for certificate in queryset:

        certificate.status = "ISSUED"

        if not certificate.issued_at:
            certificate.issued_at = timezone.now()

        certificate.revoked_reason = ""

        certificate.save()

        updated += 1

    modeladmin.message_user(
        request,
        f"{updated} certificate(s) restored."
    )


# ==================================================
# CERTIFICATE ADMIN
# ==================================================

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):

    actions = [
        issue_certificates,
        revoke_certificates,
        restore_certificates,
    ]

    list_display = (
        "certificate_number",
        "student",
        "course",
        "grade",
        "final_score",
        "status",
        "completion_date",
        "issued_at",
        "created_at",
    )

    list_filter = (
        "status",
        "grade",
        "course",
        "issued_at",
        "completion_date",
        "created_at",
    )

    search_fields = (
        "certificate_number",
        "student__username",
        "student__first_name",
        "student__last_name",
        "course",
    )

    readonly_fields = (
        "certificate_number",
        "verification_token",
        "attendance_score",
        "evaluation_score",
        "assignment_score",
        "logbook_score",
        "final_score",
        "grade",
        "issued_at",
        "created_at",
    )

    fieldsets = (

        ("Certificate Information", {
            "fields": (
                "certificate_number",
                "verification_token",
                "student",
                "trainer",
                "course",
            )
        }),

        ("Performance Scores", {
            "fields": (
                "attendance_score",
                "evaluation_score",
                "assignment_score",
                "logbook_score",
                "final_score",
                "grade",
            )
        }),

        ("Certificate Status", {
            "fields": (
                "status",
                "completion_date",
                "issued_at",
                "remarks",
                "revoked_reason",
            )
        }),

        ("System Information", {
            "fields": (
                "created_at",
            )
        }),

    )

    ordering = ("-created_at",)

    list_per_page = 25


# ==================================================
# CERTIFICATE REQUIREMENTS ADMIN
# ==================================================

@admin.register(CertificateRequirement)
class CertificateRequirementAdmin(admin.ModelAdmin):

    list_display = (
        "course",
        "min_attendance",
        "min_evaluation",
        "min_assignment",
        "min_logbook",
        "created_at",
    )

    search_fields = (
        "course",
    )

    ordering = (
        "course",
    )

    list_per_page = 25
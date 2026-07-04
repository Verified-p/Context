from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone

from .models import Certificate
from .services import CertificateService, CertificatePDFService


# ======================================
# CERTIFICATE LIST
# ======================================
@login_required
def certificate_list(request):

    if request.user.role == "STUDENT":
        certificates = Certificate.objects.filter(
            student=request.user
        ).select_related("trainer")

    else:
        certificates = Certificate.objects.select_related(
            "student",
            "trainer"
        ).all()

    return render(
        request,
        "certificate_list.html",
        {
            "certificates": certificates
        }
    )


# ======================================
# CERTIFICATE DETAIL
# ======================================
@login_required
def certificate_detail(request, pk):

    certificate = get_object_or_404(
        Certificate.objects.select_related(
            "student",
            "trainer"
        ),
        pk=pk
    )

    return render(
        request,
        "certificate_detail.html",
        {
            "certificate": certificate
        }
    )


# ======================================
# DOWNLOAD CERTIFICATE PDF
# ======================================
@login_required
def download_certificate(request, pk):

    certificate = get_object_or_404(
        Certificate.objects.select_related(
            "student",
            "trainer"
        ),
        pk=pk
    )

    if certificate.status != "ISSUED":

        messages.error(
            request,
            "Certificate has not been issued yet."
        )

        return redirect(
            "certificates:detail",
            pk=certificate.pk
        )

    pdf_buffer = (
        CertificatePDFService.generate_certificate_pdf(
            certificate
        )
    )

    response = HttpResponse(
        pdf_buffer,
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{certificate.certificate_number}.pdf"'
    )

    return response


# ======================================
# ISSUE CERTIFICATE
# ======================================
@login_required
def issue_certificate(
    request,
    student_id,
    course
):

    if request.user.role not in [
        "TRAINER",
        "SUPER_ADMIN"
    ]:
        return redirect(
            "dashboard:router"
        )

    student_model = (
        Certificate._meta
        .get_field("student")
        .related_model
    )

    student = get_object_or_404(
        student_model,
        id=student_id
    )

    certificate = (
        CertificateService.issue_certificate(
            student=student,
            trainer=request.user,
            course=course
        )
    )

    messages.success(
        request,
        f"Certificate {certificate.certificate_number} generated successfully."
    )

    return redirect(
        "certificates:detail",
        pk=certificate.pk
    )


# ======================================
# APPROVE CERTIFICATE
# ======================================
@login_required
def approve_certificate(request, pk):

    if request.user.role not in [
        "TRAINER",
        "SUPER_ADMIN"
    ]:

        messages.error(
            request,
            "You do not have permission to approve certificates."
        )

        return redirect(
            "certificates:list"
        )

    certificate = get_object_or_404(
        Certificate,
        pk=pk
    )

    certificate.status = "ISSUED"

    if not certificate.issued_at:
        certificate.issued_at = timezone.now()

    if not certificate.completion_date:
        certificate.completion_date = timezone.now().date()

    certificate.save()

    messages.success(
        request,
        f"{certificate.certificate_number} approved successfully."
    )

    return redirect(
        "certificates:detail",
        pk=certificate.pk
    )


# ======================================
# REJECT CERTIFICATE
# ======================================
@login_required
def reject_certificate(request, pk):

    if request.user.role not in [
        "TRAINER",
        "SUPER_ADMIN"
    ]:

        messages.error(
            request,
            "You do not have permission to reject certificates."
        )

        return redirect(
            "certificates:list"
        )

    certificate = get_object_or_404(
        Certificate,
        pk=pk
    )

    certificate.status = "REVOKED"

    certificate.save()

    messages.warning(
        request,
        f"{certificate.certificate_number} has been rejected."
    )

    return redirect(
        "certificates:detail",
        pk=certificate.pk
    )


# ======================================
# CERTIFICATE VERIFICATION
# ======================================
def verify_certificate(
    request,
    token
):

    certificate = get_object_or_404(
        Certificate,
        verification_token=token
    )

    return render(
        request,
        "certificate_verify.html",
        {
            "certificate": certificate,
            "valid": certificate.status == "ISSUED"
        }
    )


# ======================================
# RECOMMENDATION LETTER PAGE
# ======================================
@login_required
def recommendation_letter(
    request,
    pk
):

    certificate = get_object_or_404(
        Certificate.objects.select_related(
            "student",
            "trainer"
        ),
        pk=pk
    )

    return render(
        request,
        "recommendation_letter.html",
        {
            "certificate": certificate
        }
    )


# ======================================
# DOWNLOAD RECOMMENDATION PDF
# ======================================
@login_required
def download_recommendation(
    request,
    pk
):

    certificate = get_object_or_404(
        Certificate.objects.select_related(
            "student",
            "trainer"
        ),
        pk=pk
    )

    if certificate.status != "ISSUED":

        messages.error(
            request,
            "Recommendation letter is only available for issued certificates."
        )

        return redirect(
            "certificates:detail",
            pk=certificate.pk
        )

    from .pdf.recommendation_generator import (
        RecommendationPDFGenerator
    )

    pdf_buffer = (
        RecommendationPDFGenerator(
            certificate
        ).generate()
    )

    response = HttpResponse(
        pdf_buffer,
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="Recommendation_{certificate.certificate_number}.pdf"'
    )

    return response
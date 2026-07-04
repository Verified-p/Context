import io
import os

from django.conf import settings

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch

from .qr_generator import generate_qr


class CertificatePDFGenerator:

    def __init__(self, certificate):
        self.certificate = certificate

    def generate(self):

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=25,
            leftMargin=25,
            topMargin=25,
            bottomMargin=25
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "Title",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=30,
            textColor=colors.HexColor("#0d47a1")
        )

        center_style = ParagraphStyle(
            "Center",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=14
        )

        name_style = ParagraphStyle(
            "Name",
            parent=styles["Heading1"],
            alignment=TA_CENTER,
            fontSize=26,
            textColor=colors.HexColor("#8b0000")
        )

        elements = []

        logo_path = os.path.join(
            settings.MEDIA_ROOT,
            "branding",
            "cetms_logo.png"
        )

        trainer_signature = os.path.join(
            settings.MEDIA_ROOT,
            "branding",
            "trainer_signature.png"
        )

        director_signature = os.path.join(
            settings.MEDIA_ROOT,
            "branding",
            "director_signature.png"
        )

        stamp_path = os.path.join(
            settings.MEDIA_ROOT,
            "branding",
            "cetms_stamp.png"
        )

        if os.path.exists(logo_path):
            elements.append(
                Image(
                    logo_path,
                    width=1.2 * inch,
                    height=1.2 * inch
                )
            )

        elements.append(Spacer(1, 10))

        elements.append(
            Paragraph(
                "COMPUTERIZED E-TRAINING MANAGEMENT SYSTEM",
                center_style
            )
        )

        elements.append(
            Paragraph(
                "CERTIFICATE OF COMPLETION",
                title_style
            )
        )

        elements.append(Spacer(1, 20))

        elements.append(
            Paragraph(
                "This Certificate is Awarded To",
                center_style
            )
        )

        elements.append(Spacer(1, 15))

        student_name = (
            self.certificate.student.full_name
            or self.certificate.student.username
        )

        elements.append(
            Paragraph(
                student_name,
                name_style
            )
        )

        elements.append(Spacer(1, 15))

        elements.append(
            Paragraph(
                f"""
                For successfully completing the training programme in
                <b>{self.certificate.course}</b>
                with an overall score of
                <b>{self.certificate.final_score}%</b>.
                """,
                center_style
            )
        )

        elements.append(Spacer(1, 20))

        details = Table(
            [
                [
                    "Certificate Number",
                    self.certificate.certificate_number
                ],
                [
                    "Grade",
                    self.certificate.grade
                ],
                [
                    "Issue Date",
                    self.certificate.issued_at.strftime("%d %B %Y")
                    if self.certificate.issued_at
                    else "N/A"
                ]
            ],
            colWidths=[180, 350]
        )

        details.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ])
        )

        elements.append(details)

        elements.append(Spacer(1, 25))

        verify_url = (
            f"https://cetms.local/certificates/verify/"
            f"{self.certificate.verification_token}/"
        )

        qr = generate_qr(verify_url)

        elements.append(
            Image(
                qr,
                width=1.2 * inch,
                height=1.2 * inch
            )
        )

        elements.append(
            Paragraph(
                "Scan QR Code To Verify Authenticity",
                center_style
            )
        )

        elements.append(Spacer(1, 20))

        trainer_img = (
            Image(trainer_signature, width=100, height=40)
            if os.path.exists(trainer_signature)
            else "Trainer Signature"
        )

        director_img = (
            Image(director_signature, width=100, height=40)
            if os.path.exists(director_signature)
            else "Director Signature"
        )

        stamp_img = (
            Image(stamp_path, width=80, height=80)
            if os.path.exists(stamp_path)
            else ""
        )

        signatures = Table(
            [
                [
                    trainer_img,
                    stamp_img,
                    director_img
                ],
                [
                    "Trainer",
                    "Official Stamp",
                    "Director"
                ]
            ],
            colWidths=[220, 180, 220]
        )

        signatures.setStyle(
            TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ])
        )

        elements.append(signatures)

        doc.build(elements)

        buffer.seek(0)

        return buffer
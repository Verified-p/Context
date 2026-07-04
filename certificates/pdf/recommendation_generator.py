import io
import os

from django.conf import settings

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4


class RecommendationPDFGenerator:

    def __init__(self, certificate):
        self.certificate = certificate

    def generate(self):

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()

        heading = ParagraphStyle(
            "Heading",
            parent=styles["Heading1"],
            alignment=TA_CENTER
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

        stamp_path = os.path.join(
            settings.MEDIA_ROOT,
            "branding",
            "cetms_stamp.png"
        )

        if os.path.exists(logo_path):
            elements.append(
                Image(
                    logo_path,
                    width=70,
                    height=70
                )
            )

        elements.append(
            Paragraph(
                "LETTER OF RECOMMENDATION",
                heading
            )
        )

        elements.append(Spacer(1, 20))

        student_name = (
            self.certificate.student.full_name
            or self.certificate.student.username
        )

        trainer_name = (
            self.certificate.trainer.get_full_name()
            if self.certificate.trainer
            else "CETMS Trainer"
        )

        content = f"""
        To Whom It May Concern,<br/><br/>

        This letter serves as a formal recommendation for
        <b>{student_name}</b>,
        who successfully completed training in
        <b>{self.certificate.course}</b>
        under the Computerized E-Training Management System (CETMS).<br/><br/>

        Throughout the training period, the student demonstrated
        commitment, professionalism, discipline, teamwork,
        and strong problem-solving abilities.<br/><br/>

        The candidate achieved a final score of
        <b>{self.certificate.final_score}%</b>
        and fulfilled all academic and practical requirements.<br/><br/>

        We confidently recommend this student for employment,
        internship opportunities, industrial attachment,
        leadership roles, and further studies.<br/><br/>

        We believe the student will make a positive contribution
        to any institution or organization.<br/><br/>

        Yours faithfully,
        """

        elements.append(
            Paragraph(
                content,
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 30))

        trainer_img = (
            Image(
                trainer_signature,
                width=120,
                height=50
            )
            if os.path.exists(trainer_signature)
            else ""
        )

        stamp_img = (
            Image(
                stamp_path,
                width=80,
                height=80
            )
            if os.path.exists(stamp_path)
            else ""
        )

        signature_table = Table(
            [
                [trainer_img, stamp_img],
                [trainer_name, "Official CETMS Stamp"],
                ["Trainer / Assessor", ""]
            ],
            colWidths=[250, 150]
        )

        elements.append(signature_table)

        doc.build(elements)

        buffer.seek(0)

        return buffer
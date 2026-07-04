from datetime import datetime, timedelta
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from .models import LogbookEntry


def get_week_entries(student):
    """
    Get last 7 days entries
    """
    today = datetime.today().date()
    week_start = today - timedelta(days=7)

    return LogbookEntry.objects.filter(
        student=student,
        date__range=[week_start, today]
    )


def generate_weekly_report_pdf(student, file_path):
    """
    Generate PDF weekly report
    """

    entries = get_week_entries(student)

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph(f"Weekly Logbook Report - {student.username}", styles["Title"]))
    content.append(Spacer(1, 12))

    for e in entries:
        text = f"""
        <b>Date:</b> {e.date}<br/>
        <b>Title:</b> {e.title}<br/>
        <b>Activity:</b> {e.activity}<br/>
        <b>Status:</b> {e.status}<br/><br/>
        """
        content.append(Paragraph(text, styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)
    return file_path


def grade_log(entry):
    """
    Simple AI-like scoring system (0-100)
    """

    score = 0

    if len(entry.activity) > 50:
        score += 30

    if entry.reflection and len(entry.reflection) > 50:
        score += 30

    if entry.status == "APPROVED":
        score += 40

    return min(score, 100)
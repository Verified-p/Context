from io import BytesIO
from datetime import datetime

from django.http import HttpResponse
from django.utils import timezone

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from accounts.models import User
from attendance.models import AttendanceSession, AttendanceRecord
from assignments.models import (
    Assignment,
    AssignmentSubmission,
)


# ==========================================================
# PDF STYLES
# ==========================================================

styles = getSampleStyleSheet()

TITLE_STYLE = styles["Heading1"]
TITLE_STYLE.alignment = TA_CENTER
TITLE_STYLE.textColor = HexColor("#0d6efd")

HEADING_STYLE = styles["Heading2"]
HEADING_STYLE.textColor = HexColor("#0d6efd")

NORMAL_STYLE = styles["BodyText"]

SMALL_STYLE = styles["BodyText"]
SMALL_STYLE.fontSize = 9


# ==========================================================
# CREATE PDF DOCUMENT
# ==========================================================

def create_document(title):
    """
    Creates a ReportLab document and returns:
    buffer, document, story
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=(8.27 * inch, 11.69 * inch),   # A4
        rightMargin=25,
        leftMargin=25,
        topMargin=35,
        bottomMargin=30,
    )

    story = []

    story.append(
        Paragraph(
            "College Education & Training Management System",
            TITLE_STYLE
        )
    )

    story.append(Spacer(1, 0.20 * inch))

    story.append(
        Paragraph(
            title,
            HEADING_STYLE
        )
    )

    story.append(Spacer(1, 0.15 * inch))

    story.append(
        Paragraph(
            f"Generated on: "
            f"{timezone.localtime().strftime('%d %B %Y %I:%M %p')}",
            SMALL_STYLE
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    return buffer, document, story


# ==========================================================
# TABLE STYLE
# ==========================================================

def default_table_style():

    return TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#0d6efd")),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("FONTSIZE", (0, 0), (-1, -1), 10),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

    ])


# ==========================================================
# BUILD PDF RESPONSE
# ==========================================================

def build_pdf(document, buffer, story, filename):
    """
    Finalizes the PDF and returns HttpResponse.
    """

    document.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    response.write(pdf)

    return response


# ==========================================================
# SUMMARY CARD
# ==========================================================

def add_summary(story, title, value):

    table = Table(
        [
            [title],
            [str(value)]
        ],
        colWidths=[220]
    )

    table.setStyle(
        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#198754")),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ("BACKGROUND", (0, 1), (-1, 1), colors.beige),

            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ])
    )

    story.append(table)

    story.append(Spacer(1, 0.20 * inch))

# ==========================================================
# STUDENT REPORT PDF
# ==========================================================

def student_report_pdf(request):
    """
    Generate Student Report PDF.
    Trainers and Super Admins can generate this report.
    """

    if not (
        request.user.is_staff or
        request.user.role in ["SUPER_ADMIN", "TRAINER"]
    ):
        return HttpResponse(
            "You are not authorized to access this report.",
            status=403
        )

    students = (
        User.objects
        .filter(role="STUDENT")
        .order_by("first_name", "last_name", "username")
    )

    total_students = students.count()

    verified_students = students.filter(
        is_verified=True
    ).count()

    unverified_students = total_students - verified_students

    active_students = students.filter(
        is_active=True
    ).count()

    buffer, document, story = create_document(
        "Student Report"
    )

    # ------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "<b>Report Summary</b>",
            HEADING_STYLE
        )
    )

    story.append(Spacer(1, 10))

    summary = [

        ["Statistic", "Value"],

        ["Total Students", str(total_students)],

        ["Verified Students", str(verified_students)],

        ["Unverified Students", str(unverified_students)],

        ["Active Students", str(active_students)],

    ]

    summary_table = Table(
        summary,
        colWidths=[250, 120]
    )

    summary_table.setStyle(
        default_table_style()
    )

    story.append(summary_table)

    story.append(Spacer(1, 25))

    # ------------------------------------------------------
    # STUDENT LIST
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "<b>Student List</b>",
            HEADING_STYLE
        )
    )

    story.append(Spacer(1, 10))

    table_data = [

        [
            "#",
            "Admission",
            "Student Name",
            "Email",
            "Phone",
            "Verified",
            "Status",
        ]

    ]

    for index, student in enumerate(
        students,
        start=1
    ):

        full_name = (
            student.get_full_name().strip()
            or student.username
        )

        table_data.append([

            str(index),

            student.username,

            full_name,

            student.email or "-",

            student.phone_number or "-",

            "Yes" if student.is_verified else "No",

            "Active" if student.is_active else "Inactive",

        ])

    student_table = Table(
        table_data,
        colWidths=[
            30,
            70,
            120,
            140,
            80,
            50,
            55,
        ]
    )

    student_table.setStyle(
        default_table_style()
    )

    story.append(student_table)

    story.append(Spacer(1, 20))

    # ------------------------------------------------------
    # FOOTER
    # ------------------------------------------------------

    story.append(
        Paragraph(
            f"End of Student Report • Generated by {request.user.get_full_name() or request.user.username}",
            SMALL_STYLE
        )
    )

    return build_pdf(
        document=document,
        buffer=buffer,
        story=story,
        filename="Student_Report.pdf"
    )

# ==========================================================
# ATTENDANCE REPORT PDF
# ==========================================================

def attendance_report_pdf(request):
    """
    Generate Attendance Session Report PDF.
    Shows one row per attendance session.
    """

    if not (
        request.user.is_staff or
        request.user.role in ["SUPER_ADMIN", "TRAINER"]
    ):
        return HttpResponse(
            "You are not authorized to access this report.",
            status=403
        )

    sessions = (
        AttendanceSession.objects
        .select_related("created_by")
        .prefetch_related("records")
        .order_by("-created_at")
    )

    total_sessions = sessions.count()

    active_sessions = sessions.filter(
        is_active=True
    ).count()

    closed_sessions = total_sessions - active_sessions

    total_attendance = AttendanceRecord.objects.count()

    buffer, document, story = create_document(
        "Attendance Sessions Report"
    )

    # ======================================================
    # REPORT SUMMARY
    # ======================================================

    story.append(
        Paragraph(
            "<b>Attendance Summary</b>",
            HEADING_STYLE
        )
    )

    story.append(Spacer(1, 10))

    summary = [

        ["Statistic", "Value"],

        ["Total Sessions", str(total_sessions)],

        ["Active Sessions", str(active_sessions)],

        ["Closed Sessions", str(closed_sessions)],

        ["Attendance Records", str(total_attendance)],

    ]

    summary_table = Table(
        summary,
        colWidths=[260, 120]
    )

    summary_table.setStyle(
        default_table_style()
    )

    story.append(summary_table)

    story.append(Spacer(1, 20))

    # ======================================================
    # SESSION TABLE
    # ======================================================

    story.append(
        Paragraph(
            "<b>Attendance Sessions</b>",
            HEADING_STYLE
        )
    )

    story.append(Spacer(1, 10))

    table_data = [[

        "#",
        "Title",
        "Course",
        "Trainer",
        "Students",
        "Status",
        "Created"

    ]]

    for index, session in enumerate(
        sessions,
        start=1
    ):

        trainer = (
            session.created_by.get_full_name()
            or session.created_by.username
        )

        status = (
            "Active"
            if session.is_active
            else "Closed"
        )

        table_data.append([

            str(index),

            session.title,

            session.course or "-",

            trainer,

            str(session.total_attendees),

            status,

            session.created_at.strftime(
                "%d/%m/%Y"
            ),

        ])

    table = Table(
        table_data,
        colWidths=[
            25,
            120,
            80,
            110,
            50,
            55,
            70,
        ]
    )

    table.setStyle(
        default_table_style()
    )

    story.append(table)

    story.append(Spacer(1, 25))

    # ======================================================
    # FOOTER
    # ======================================================

    story.append(
        Paragraph(
            f"Generated by: {request.user.get_full_name() or request.user.username}",
            SMALL_STYLE
        )
    )

    story.append(
        Paragraph(
            timezone.localtime().strftime(
                "%d %B %Y %I:%M %p"
            ),
            SMALL_STYLE
        )
    )

    return build_pdf(
        document=document,
        buffer=buffer,
        story=story,
        filename="Attendance_Report.pdf"
    )

# ==========================================================
# ASSIGNMENT REPORT PDF
# ==========================================================

def assignment_report_pdf(request):
    """
    Generate Assignment Report PDF.
    Only Trainers and Super Admins can generate this report.
    """

    if not (
        request.user.is_staff or
        request.user.role in ["SUPER_ADMIN", "TRAINER"]
    ):
        return HttpResponse(
            "You are not authorized to access this report.",
            status=403
        )

    assignments = (
        Assignment.objects
        .select_related("lesson", "created_by")
        .prefetch_related("submissions")
        .order_by("-created_at")
    )

    total_assignments = assignments.count()

    published = assignments.filter(
        status="PUBLISHED"
    ).count()

    drafts = assignments.filter(
        status="DRAFT"
    ).count()

    closed = assignments.filter(
        status="CLOSED"
    ).count()

    total_submissions = AssignmentSubmission.objects.count()

    graded = AssignmentSubmission.objects.filter(
        status="GRADED"
    ).count()

    late = AssignmentSubmission.objects.filter(
        is_late=True
    ).count()

    buffer, document, story = create_document(
        "Assignment Report"
    )

    # ======================================================
    # SUMMARY
    # ======================================================

    story.append(
        Paragraph(
            "<b>Assignment Summary</b>",
            HEADING_STYLE
        )
    )

    story.append(Spacer(1, 10))

    summary = [

        ["Statistic", "Value"],

        ["Total Assignments", total_assignments],

        ["Published", published],

        ["Drafts", drafts],

        ["Closed", closed],

        ["Total Submissions", total_submissions],

        ["Graded", graded],

        ["Late Submissions", late],

    ]

    summary_table = Table(
        summary,
        colWidths=[250, 120]
    )

    summary_table.setStyle(
        default_table_style()
    )

    story.append(summary_table)

    story.append(Spacer(1, 20))

    # ======================================================
    # ASSIGNMENT TABLE
    # ======================================================

    story.append(
        Paragraph(
            "<b>Assignment List</b>",
            HEADING_STYLE
        )
    )

    story.append(Spacer(1, 10))

    table_data = [[

        "#",
        "Assignment",
        "Lesson",
        "Marks",
        "Due Date",
        "Submissions",
        "Status",

    ]]

    for index, assignment in enumerate(
        assignments,
        start=1
    ):

        lesson = "-"

        if assignment.lesson:
            lesson = str(assignment.lesson)

        table_data.append([

            str(index),

            assignment.title,

            lesson,

            str(assignment.total_marks),

            assignment.due_date.strftime("%d/%m/%Y"),

            str(assignment.total_submissions),

            assignment.status,

        ])

    assignment_table = Table(
        table_data,
        colWidths=[
            25,
            140,
            110,
            45,
            70,
            60,
            60,
        ]
    )

    assignment_table.setStyle(
        default_table_style()
    )

    story.append(assignment_table)

    story.append(Spacer(1, 25))

    # ======================================================
    # FOOTER
    # ======================================================

    story.append(
        Paragraph(
            f"Generated by: {request.user.get_full_name() or request.user.username}",
            SMALL_STYLE
        )
    )

    story.append(
        Paragraph(
            timezone.localtime().strftime(
                "%d %B %Y %I:%M %p"
            ),
            SMALL_STYLE
        )
    )

    return build_pdf(
        document=document,
        buffer=buffer,
        story=story,
        filename="Assignment_Report.pdf"
    )

# ==========================================================
# SYSTEM ANALYTICS PDF
# ==========================================================

def analytics_report_pdf(request):
    """
    Generate System Analytics Report PDF.
    Accessible to Super Admins and Trainers.
    """

    if not (
        request.user.is_staff or
        request.user.role in ["SUPER_ADMIN", "TRAINER"]
    ):
        return HttpResponse(
            "You are not authorized to access this report.",
            status=403
        )

    # ======================================================
    # USER STATISTICS
    # ======================================================

    total_users = User.objects.count()

    total_students = User.objects.filter(
        role="STUDENT"
    ).count()

    total_trainers = User.objects.filter(
        role="TRAINER"
    ).count()

    total_admins = User.objects.filter(
        role="SUPER_ADMIN"
    ).count()

    verified_users = User.objects.filter(
        is_verified=True
    ).count()

    # ======================================================
    # ATTENDANCE STATISTICS
    # ======================================================

    total_sessions = AttendanceSession.objects.count()

    active_sessions = AttendanceSession.objects.filter(
        is_active=True
    ).count()

    attendance_records = AttendanceRecord.objects.count()

    present_count = AttendanceRecord.objects.filter(
        status="PRESENT"
    ).count()

    late_count = AttendanceRecord.objects.filter(
        status="LATE"
    ).count()

    absent_count = AttendanceRecord.objects.filter(
        status="ABSENT"
    ).count()

    attendance_rate = 0

    if attendance_records > 0:
        attendance_rate = round(
            (present_count / attendance_records) * 100,
            1
        )

    # ======================================================
    # ASSIGNMENT STATISTICS
    # ======================================================

    total_assignments = Assignment.objects.count()

    published_assignments = Assignment.objects.filter(
        status="PUBLISHED"
    ).count()

    total_submissions = AssignmentSubmission.objects.count()

    graded_submissions = AssignmentSubmission.objects.filter(
        status="GRADED"
    ).count()

    late_submissions = AssignmentSubmission.objects.filter(
        is_late=True
    ).count()

    average_score = 0

    graded = AssignmentSubmission.objects.exclude(
        marks_awarded=None
    )

    if graded.exists():

        total_marks = sum(
            float(s.marks_awarded)
            for s in graded
        )

        total_possible = sum(
            s.assignment.total_marks
            for s in graded
        )

        if total_possible > 0:
            average_score = round(
                (total_marks / total_possible) * 100,
                1
            )

    # ======================================================
    # CREATE DOCUMENT
    # ======================================================

    buffer, document, story = create_document(
        "System Analytics Report"
    )

    story.append(
        Paragraph(
            "<b>Overall System Statistics</b>",
            HEADING_STYLE
        )
    )

    story.append(Spacer(1, 10))

    analytics = [

        ["Category", "Value"],

        ["Total Users", total_users],

        ["Students", total_students],

        ["Trainers", total_trainers],

        ["Administrators", total_admins],

        ["Verified Users", verified_users],

        ["Attendance Sessions", total_sessions],

        ["Active Sessions", active_sessions],

        ["Attendance Records", attendance_records],

        ["Present", present_count],

        ["Late", late_count],

        ["Absent", absent_count],

        ["Attendance Rate", f"{attendance_rate}%"],

        ["Assignments", total_assignments],

        ["Published Assignments", published_assignments],

        ["Assignment Submissions", total_submissions],

        ["Graded Submissions", graded_submissions],

        ["Late Submissions", late_submissions],

        ["Average Assignment Score", f"{average_score}%"],

    ]

    table = Table(
        analytics,
        colWidths=[250, 180]
    )

    table.setStyle(
        default_table_style()
    )

    story.append(table)

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>System Summary</b>",
            HEADING_STYLE
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "This report summarizes the overall status of the "
            "College Education & Training Management System "
            "(CETMS), including users, attendance, assignments "
            "and student performance.",
            NORMAL_STYLE
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Generated by: "
            f"{request.user.get_full_name() or request.user.username}",
            SMALL_STYLE
        )
    )

    story.append(
        Paragraph(
            timezone.localtime().strftime(
                "%d %B %Y %I:%M %p"
            ),
            SMALL_STYLE
        )
    )

    return build_pdf(
        document=document,
        buffer=buffer,
        story=story,
        filename="System_Analytics_Report.pdf"
    )
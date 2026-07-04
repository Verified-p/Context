from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [

    # =====================================================
    # REPORTS HOME
    # =====================================================
    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    # =====================================================
    # STUDENT REPORTS
    # =====================================================
    path(
        "students/",
        views.student_reports,
        name="student_reports"
    ),

    # =====================================================
    # ATTENDANCE REPORTS
    # =====================================================
    path(
        "attendance/",
        views.attendance_reports,
        name="attendance_reports"
    ),

    # =====================================================
    # ASSIGNMENT REPORTS
    # =====================================================
    path(
        "assignments/",
        views.assignment_reports,
        name="assignment_reports"
    ),

    # =====================================================
    # FINANCE REPORTS
    # =====================================================
    path(
        "finance/",
        views.finance_reports,
        name="finance_reports"
    ),

    # =====================================================
    # ANALYTICS
    # =====================================================
    path(
        "analytics/",
        views.analytics,
        name="analytics"
    ),

]
from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [

    # ==========================
    # DASHBOARD
    # ==========================
    path(
        "dashboard/",
        views.attendance_dashboard,
        name="dashboard"
    ),

    # ==========================
    # CREATE SESSION
    # ==========================
    path(
        "create/",
        views.create_session,
        name="create"
    ),

    # ==========================
    # SESSION DETAILS
    # ==========================
    path(
        "session/<int:pk>/",
        views.session_detail,
        name="session_detail"
    ),

    # ==========================
    # QR SCAN
    # ==========================
    path(
        "scan/<uuid:token>/",
        views.scan_qr,
        name="scan"
    ),

    # ==========================
    # REPORTS
    # ==========================
    path(
        "report/",
        views.attendance_report,
        name="report"
    ),

    # ==========================
    # STATISTICS
    # ==========================
    path(
        "stats/",
        views.attendance_stats,
        name="stats"
    ),

]
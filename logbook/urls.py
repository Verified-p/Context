from django.urls import path

from . import views
from .callback import onlyoffice_callback

app_name = "logbook"

urlpatterns = [

    # ==========================================
    # STUDENT LOGBOOK
    # ==========================================

    path(
        "upload/",
        views.upload_logbook,
        name="upload_logbook"
    ),

    path(
        "edit/",
        views.edit_logbook,
        name="edit_logbook"
    ),

    # ==========================================
    # TRAINER / ADMIN VIEW LOGBOOK
    # ==========================================

    path(
        "view/<int:pk>/",
        views.view_logbook,
        name="view_logbook"
    ),

    # ==========================================
    # REVIEW LOGBOOK
    # ==========================================

    path(
        "review/<int:pk>/",
        views.supervisor_review,
        name="supervisor_review"
    ),

    # ==========================================
    # ONLYOFFICE CALLBACK
    # ==========================================

    path(
        "callback/<int:logbook_id>/",
        onlyoffice_callback,
        name="onlyoffice_callback"
    ),

    # ==========================================
    # STUDENT DASHBOARD
    # ==========================================

    path(
        "create/",
        views.create_entry,
        name="create_entry"
    ),

    path(
        "entries/",
        views.daily_entries,
        name="daily_entries"
    ),

    # ==========================================
    # REPORTS
    # ==========================================

    path(
        "monthly/",
        views.monthly_summary,
        name="monthly_summary"
    ),

    path(
        "report/",
        views.logbook_report,
        name="report"
    ),

    path(
        "weekly-report/",
        views.download_weekly_report,
        name="weekly_report"
    ),

    path(
    "submit/<int:pk>/",
    views.submit_logbook,
    name="submit_logbook"
),

]


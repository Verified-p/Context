from django.urls import path
from . import views

app_name = "certificates"

urlpatterns = [

    # =========================
    # CERTIFICATE LIST
    # =========================
    path(
        "",
        views.certificate_list,
        name="list"
    ),

    # =========================
    # CERTIFICATE DETAILS
    # =========================
    path(
        "<int:pk>/",
        views.certificate_detail,
        name="detail"
    ),

    # =========================
    # DOWNLOAD CERTIFICATE
    # =========================
    path(
        "download/<int:pk>/",
        views.download_certificate,
        name="download"
    ),

    # =========================
    # ISSUE CERTIFICATE
    # =========================
    path(
        "issue/<int:student_id>/<str:course>/",
        views.issue_certificate,
        name="issue"
    ),

    # =========================
    # RECOMMENDATION LETTER
    # =========================
    path(
        "recommendation/<int:pk>/",
        views.recommendation_letter,
        name="recommendation"
    ),

    # =========================
    # CERTIFICATE VERIFICATION
    # =========================
    path(
        "verify/<uuid:token>/",
        views.verify_certificate,
        name="verify"
    ),
    # =========================
# APPROVE CERTIFICATE
# =========================
path(
    "approve/<int:pk>/",
    views.approve_certificate,
    name="approve"
),

# =========================
# REJECT CERTIFICATE
# =========================
path(
    "reject/<int:pk>/",
    views.reject_certificate,
    name="reject"
),
path(
    "recommendation/download/<int:pk>/",
    views.download_recommendation,
    name="download_recommendation"
),

]
from django.urls import path
from . import views

app_name = "students"

urlpatterns = [

    # ==========================================
    # STUDENT REGISTRATION
    # ==========================================
    path(
        "register/",
        views.register_student,
        name="register"
    ),



path(
    "self-register/",
    views.student_register,
    name="self_register"
),

    # ==========================================
    # STUDENT DASHBOARD & PROFILE
    # ==========================================
    path(
        "dashboard/",
        views.student_dashboard,
        name="dashboard"
    ),

    path(
        "profile/",
        views.student_profile,
        name="profile"
    ),

    # ==========================================
    # STUDENT MANAGEMENT
    # ==========================================
    path(
        "list/",
        views.student_list,
        name="list"
    ),

    path(
        "detail/<int:pk>/",
        views.student_detail,
        name="detail"
    ),

    # ==========================================
    # APPROVALS
    # ==========================================
    path(
        "pending/",
        views.pending_approvals,
        name="pending_approvals"
    ),

    path(
        "approved/",
        views.approved_students,
        name="approved_students"
    ),

    path(
        "approve/<int:pk>/",
        views.approve_student_view,
        name="approve"
    ),

    path(
        "reject/<int:pk>/",
        views.reject_student_view,
        name="reject"
    ),
]
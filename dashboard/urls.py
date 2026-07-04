from django.urls import path

from .views import (
    dashboard_router,
    admin_dashboard,
    trainer_dashboard,
    student_dashboard,
    finance_dashboard,
)

app_name = "dashboard"

urlpatterns = [

    # ==========================================
    # Dashboard Router
    # ==========================================

    path(
        "",
        dashboard_router,
        name="router",
    ),

    # ==========================================
    # Super Admin Dashboard
    # ==========================================

    path(
        "admin/",
        admin_dashboard,
        name="admin_dashboard",
    ),

    # ==========================================
    # Trainer Dashboard
    # ==========================================

    path(
        "trainer/",
        trainer_dashboard,
        name="trainer_dashboard",
    ),

    # ==========================================
    # Student Dashboard
    # ==========================================

    path(
        "student/",
        student_dashboard,
        name="student_dashboard",
    ),

    # ==========================================
    # Finance Dashboard
    # ==========================================

    path(
        "finance/",
        finance_dashboard,
        name="finance_dashboard",
    ),

]
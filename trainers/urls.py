from django.urls import path
from . import views

app_name = "trainers"

urlpatterns = [
    path(
        "dashboard/",
        views.trainer_dashboard,
        name="dashboard"
    ),

    path(
        "students/",
        views.trainer_students,
        name="students"
    ),

    path(
        "assignments/",
        views.trainer_assignments,
        name="assignments"
    ),

    path(
        "profile/",
        views.trainer_profile,
        name="profile"
    ),

    path(
        "generate-certificate/<int:student_id>/",
        views.generate_certificate,
        name="generate_certificate"
    ),
]
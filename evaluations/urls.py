from django.urls import path
from . import views

app_name = "evaluations"

urlpatterns = [
    path("", views.evaluation_list, name="list"),
    path("evaluate/", views.evaluate_student, name="evaluate"),
    path("dashboard/", views.evaluation_dashboard, name="dashboard"),
    path("report/<int:pk>/", views.evaluation_report, name="report"),
    path("summary/", views.evaluation_summary, name="summary"),
    path(
    "analytics/",
    views.analytics,
    name="analytics"
),
]
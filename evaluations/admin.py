from django.contrib import admin
from .models import Evaluation


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "lesson",
        "trainer",
        "total_score",
        "status",
        "created_at"
    )

    list_filter = ("status", "lesson")
    search_fields = ("student__username", "lesson__title")
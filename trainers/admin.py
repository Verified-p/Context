from django.contrib import admin
from .models import TrainerProfile


@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "department",
    )

    search_fields = (
        "user__username",
        "user__email",
        "department",
    )

    list_filter = (
        "department",
    )
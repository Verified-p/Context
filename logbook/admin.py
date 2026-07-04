from django.contrib import admin
from .models import LogbookEntry


@admin.register(LogbookEntry)
class LogbookEntryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student",
        "title",
        "date",
        "status",
        "reviewed_by",
    )

    list_filter = ("status", "date")

    search_fields = (
        "student__username",
        "title",
        "activity",
    )
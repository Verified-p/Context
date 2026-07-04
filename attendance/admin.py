from django.contrib import admin

from .models import AttendanceSession
from .models import AttendanceRecord


# ==========================================
# ATTENDANCE SESSION ADMIN
# ==========================================

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "course",
        "created_by",
        "is_active",
        "created_at",
        "expires_at",
        "total_attendees",
    )

    list_filter = (
        "is_active",
        "course",
        "created_at",
    )

    search_fields = (
        "title",
        "course",
        "created_by__username",
    )

    readonly_fields = (
        "session_token",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )


# ==========================================
# ATTENDANCE RECORD ADMIN
# ==========================================

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student",
        "session",
        "status",
        "timestamp",
    )

    list_filter = (
        "status",
        "session",
        "timestamp",
    )

    search_fields = (
        "student__username",
        "student__first_name",
        "student__last_name",
        "session__title",
    )

    ordering = (
        "-timestamp",
    )
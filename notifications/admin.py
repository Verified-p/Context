from django.contrib import admin

from .models import (
    Notification,
    Announcement,
    Reminder,
    Broadcast,
)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "recipient",
        "notification_type",
        "priority",
        "is_read",
        "created_at",
    )

    list_filter = (
        "notification_type",
        "priority",
        "is_read",
    )

    search_fields = (
        "title",
        "message",
        "recipient__username",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "target_role",
        "priority",
        "is_active",
        "created_at",
    )

    list_filter = (
        "target_role",
        "priority",
        "is_active",
    )


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "recipient",
        "remind_at",
        "is_sent",
        "is_read",
    )

    list_filter = (
        "is_sent",
        "is_read",
    )


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "target_role",
        "priority",
        "is_active",
        "created_at",
    )

    list_filter = (
        "target_role",
        "priority",
        "is_active",
    )
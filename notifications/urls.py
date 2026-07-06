# notifications/urls.py

from django.urls import path

from .views import (
    notifications,
    announcements,
    reminders,
    broadcasts,
    mark_as_read,
    mark_all_as_read,
    archive_notification,
    delete_notification,
)

app_name = "notifications"

urlpatterns = [

    # ==========================================================
    # NOTIFICATIONS
    # ==========================================================

    path(
        "",
        notifications,
        name="list",
    ),

    # ==========================================================
    # ANNOUNCEMENTS
    # ==========================================================

    path(
        "announcements/",
        announcements,
        name="announcements",
    ),

    # ==========================================================
    # REMINDERS
    # ==========================================================

    path(
        "reminders/",
        reminders,
        name="reminders",
    ),

    # ==========================================================
    # BROADCASTS
    # ==========================================================

    path(
        "broadcasts/",
        broadcasts,
        name="broadcasts",
    ),

    # ==========================================================
    # NOTIFICATION ACTIONS
    # ==========================================================

    path(
        "read/<int:pk>/",
        mark_as_read,
        name="mark_read",
    ),

    path(
        "read-all/",
        mark_all_as_read,
        name="mark_all_read",
    ),

    path(
        "archive/<int:pk>/",
        archive_notification,
        name="archive",
    ),

    path(
        "delete/<int:pk>/",
        delete_notification,
        name="delete",
    ),

]
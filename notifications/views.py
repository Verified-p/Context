# notifications/views.py

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from .models import (
    Notification,
    Announcement,
    Reminder,
    Broadcast,
)


# ==========================================================
# ALL NOTIFICATIONS
# ==========================================================

@login_required
def notifications(request):

    notifications = (
        Notification.objects
        .filter(
            recipient=request.user,
            is_deleted=False
        )
        .order_by("-created_at")
    )

    unread_count = notifications.filter(
        is_read=False
    ).count()

    context = {

        "notifications": notifications,

        "unread_count": unread_count,

    }

    return render(
        request,
        "notifications.html",
        context
    )


# ==========================================================
# ANNOUNCEMENTS
# ==========================================================

@login_required
def announcements(request):

    announcements = Announcement.objects.filter(
        is_active=True
    )

    announcements = announcements.filter(
        target_role__in=[
            "ALL",
            request.user.role
        ]
    )

    context = {

        "announcements": announcements,

    }

    return render(
        request,
        "announcements.html",
        context
    )


# ==========================================================
# REMINDERS
# ==========================================================

@login_required
def reminders(request):

    reminders = Reminder.objects.filter(
        recipient=request.user
    ).order_by("remind_at")

    context = {

        "reminders": reminders,

    }

    return render(
        request,
        "reminders.html",
        context
    )


# ==========================================================
# BROADCASTS
# ==========================================================

@login_required
def broadcasts(request):

    broadcasts = Broadcast.objects.filter(
        is_active=True
    )

    broadcasts = broadcasts.filter(
        target_role__in=[
            "ALL",
            request.user.role
        ]
    )

    context = {

        "broadcasts": broadcasts,

    }

    return render(
        request,
        "broadcasts.html",
        context
    )


# ==========================================================
# MARK ONE NOTIFICATION AS READ
# ==========================================================

@login_required
def mark_as_read(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user
    )

    notification.mark_as_read()

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "notifications:list"
        )
    )


# ==========================================================
# MARK ALL NOTIFICATIONS AS READ
# ==========================================================

@login_required
def mark_all_as_read(request):

    unread_notifications = Notification.objects.filter(
        recipient=request.user,
        is_read=False,
        is_deleted=False
    )

    for notification in unread_notifications:

        notification.mark_as_read()

    messages.success(
        request,
        "All notifications have been marked as read."
    )

    return redirect(
        "notifications:list"
    )


# ==========================================================
# ARCHIVE NOTIFICATION
# ==========================================================

@login_required
def archive_notification(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user
    )

    notification.archive()

    messages.success(
        request,
        "Notification archived successfully."
    )

    return redirect(
        "notifications:list"
    )


# ==========================================================
# DELETE NOTIFICATION
# ==========================================================

@login_required
def delete_notification(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user
    )

    notification.soft_delete()

    messages.success(
        request,
        "Notification deleted successfully."
    )

    return redirect(
        "notifications:list"
    )
# notifications/context_processors.py

from .models import Notification


def notification_context(request):
    """
    Makes notifications available in every template.

    Automatically provides:
    - unread notification count
    - latest notifications
    - total notifications
    """

    if not request.user.is_authenticated:

        return {

            "navbar_notifications": [],

            "navbar_notification_count": 0,

            "navbar_total_notifications": 0,

        }

    notifications = (
        Notification.objects
        .filter(
            recipient=request.user,
            is_deleted=False
        )
        .select_related("sender")
        .order_by("-created_at")
    )

    unread_notifications = notifications.filter(
        is_read=False
    )

    return {

        "navbar_notifications": notifications[:8],

        "navbar_notification_count": unread_notifications.count(),

        "navbar_total_notifications": notifications.count(),

    }
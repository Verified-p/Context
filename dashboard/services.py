# dashboard/services.py

from django.urls import reverse


def get_dashboard_url(user):
    """
    Returns the appropriate dashboard URL
    based on the logged-in user's role.
    """

    # User must be authenticated
    if not user.is_authenticated:
        return reverse("accounts:login")

    # Prevent inactive or locked accounts
    if not user.is_active:
        return reverse("accounts:login")

    role = getattr(user, "role", "").upper()

    dashboard_map = {

        "SUPER_ADMIN": "dashboard:admin_dashboard",

        "TRAINER": "dashboard:trainer_dashboard",

        "STUDENT": "dashboard:student_dashboard",

        "FINANCE": "dashboard:finance_dashboard",

    }

    return reverse(
        dashboard_map.get(
            role,
            "accounts:login"
        )
    )
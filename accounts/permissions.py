# accounts/permissions.py

from functools import wraps

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


def role_required(allowed_roles=None):
    """
    Generic role-based permission decorator
    """

    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):

        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if request.user.role in allowed_roles:
                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            raise PermissionDenied(
                "You do not have permission to access this page."
            )

        return wrapper

    return decorator


def super_admin_required(view_func):
    """
    Super Admin Only
    """

    return role_required(
        ['SUPER_ADMIN']
    )(view_func)


def trainer_required(view_func):
    """
    Trainer Only
    """

    return role_required(
        ['TRAINER']
    )(view_func)


def student_required(view_func):
    """
    Student Only
    """

    return role_required(
        ['STUDENT']
    )(view_func)


def finance_required(view_func):
    """
    Finance Officer Only
    """

    return role_required(
        ['FINANCE']
    )(view_func)


def admin_or_trainer_required(view_func):
    """
    Super Admin + Trainer
    """

    return role_required(
        [
            'SUPER_ADMIN',
            'TRAINER'
        ]
    )(view_func)


def admin_or_finance_required(view_func):
    """
    Super Admin + Finance
    """

    return role_required(
        [
            'SUPER_ADMIN',
            'FINANCE'
        ]
    )(view_func)


def staff_required(view_func):
    """
    Internal staff only
    """

    return role_required(
        [
            'SUPER_ADMIN',
            'TRAINER',
            'FINANCE'
        ]
    )(view_func)
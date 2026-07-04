# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    EmailVerification,
    LoginActivity,
    AuditLog
)


# =====================================================
# USER ADMIN
# =====================================================

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'is_active',
        'is_verified',
        'is_locked',
        'last_seen',
        'date_joined',
    )

    list_filter = (
        'role',
        'is_active',
        'is_verified',
        'is_locked',
        'date_joined',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'phone_number',
    )

    ordering = (
        '-date_joined',
    )

    readonly_fields = (
        'last_seen',
        'created_at',
        'updated_at',
        'failed_login_attempts',
    )

    fieldsets = (

        ('Authentication', {
            'fields': (
                'username',
                'password',
            )
        }),

        ('Personal Information', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone_number',
                'profile_picture',
            )
        }),

        ('Role & Status', {
            'fields': (
                'role',
                'is_verified',
                'is_locked',
                'failed_login_attempts',
            )
        }),

        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),

        ('Tracking', {
            'fields': (
                'last_login',
                'last_seen',
                'created_at',
                'updated_at',
            )
        }),

    )

    add_fieldsets = (

        ('Create User', {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'role',
                'password1',
                'password2',
            ),
        }),

    )


# =====================================================
# EMAIL VERIFICATION
# =====================================================

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'token',
        'is_verified',
        'created_at',
        'verified_at',
    )

    list_filter = (
        'is_verified',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
    )

    readonly_fields = (
        'token',
        'created_at',
        'verified_at',
    )


# =====================================================
# LOGIN ACTIVITY
# =====================================================

@admin.register(LoginActivity)
class LoginActivityAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'ip_address',
        'success',
        'login_time',
    )

    list_filter = (
        'success',
        'login_time',
    )

    search_fields = (
        'user__username',
        'ip_address',
    )

    ordering = (
        '-login_time',
    )

    readonly_fields = (
        'user',
        'ip_address',
        'browser',
        'login_time',
        'success',
    )


# =====================================================
# AUDIT LOGS
# =====================================================

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'action',
        'timestamp',
    )

    list_filter = (
        'action',
        'timestamp',
    )

    search_fields = (
        'user__username',
        'description',
    )

    ordering = (
        '-timestamp',
    )

    readonly_fields = (
        'user',
        'action',
        'description',
        'timestamp',
    )
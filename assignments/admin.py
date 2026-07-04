from django.contrib import admin

from .models import (
    Assignment,
    AssignmentSubmission
)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'assignment_code',
        'lesson',
        'status',
        'total_marks',
        'due_date',
        'created_by',
        'created_at'
    )

    list_filter = (
        'status',
        'created_at',
        'due_date'
    )

    search_fields = (
        'title',
        'assignment_code'
    )

    ordering = (
        '-created_at',
    )


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):

    list_display = (
        'assignment',
        'student',
        'submitted_at',
        'is_late',
        'marks_awarded',
        'status'
    )

    list_filter = (
        'status',
        'is_late'
    )

    search_fields = (
        'student__username',
        'assignment__title'
    )

    ordering = (
        '-submitted_at',
    )
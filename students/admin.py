from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'national_id',
        'course',
        'training_mode',
        'status',
        'created_at'
    )

    list_filter = ('status', 'training_mode', 'session')

    search_fields = ('full_name', 'national_id', 'course')
from django.contrib import admin
from .models import Lesson, LessonProgress


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):

    list_display = ('title', 'lesson_code', 'status', 'created_by')
    list_filter = ('status',)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):

    list_display = ('student', 'lesson', 'status', 'updated_at')
    list_filter = ('status',)
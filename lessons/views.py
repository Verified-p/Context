from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Lesson, LessonProgress
from .forms import LessonForm
from .services import publish_lesson, draft_lesson


# ===================================
# LESSON LIST
# ===================================

@login_required
def lesson_list(request):

    lessons = (
        Lesson.objects
        .filter(status="PUBLISHED")
        .select_related("created_by")
        .order_by("lesson_date", "start_time", "-created_at")
    )

    return render(request, "lesson_list.html", {
        "lessons": lessons,
        "today": timezone.localdate(),
        "now": timezone.localtime(),
    })


# ===================================
# LESSON DETAIL
# ===================================

@login_required
def lesson_detail(request, pk):

    lesson = get_object_or_404(
        Lesson.objects.select_related("created_by"),
        pk=pk
    )

    progress = None

    # Only students get lesson progress
    if request.user != lesson.created_by:

        progress, created = LessonProgress.objects.get_or_create(
            student=request.user,
            lesson=lesson,
            defaults={
                "status": "IN_PROGRESS"
            }
        )

        if not created and progress.status == "NOT_STARTED":
            progress.status = "IN_PROGRESS"

        if lesson.lesson_type == "LIVE":
            progress.joined_live = True

        progress.save()

    return render(request, "lesson_detail.html", {
        "lesson": lesson,
        "progress": progress,
        "today": timezone.localdate(),
        "now": timezone.localtime(),
    })


# ===================================
# CREATE LESSON
# ===================================

@login_required
def create_lesson(request):

    if request.method == "POST":

        form = LessonForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            lesson = form.save(commit=False)

            lesson.created_by = request.user

            lesson.save()

            if lesson.status == "PUBLISHED":
                publish_lesson(lesson)
            else:
                draft_lesson(lesson)

            return redirect("lessons:lesson_list")

    else:

        form = LessonForm()

    return render(request, "create_lesson.html", {
        "form": form
    })


# ===================================
# EDIT LESSON
# ===================================

@login_required
def edit_lesson(request, pk):

    lesson = get_object_or_404(
        Lesson,
        pk=pk,
        created_by=request.user
    )

    if request.method == "POST":

        form = LessonForm(
            request.POST,
            request.FILES,
            instance=lesson
        )

        if form.is_valid():

            lesson = form.save()

            if lesson.status == "PUBLISHED":
                publish_lesson(lesson)
            else:
                draft_lesson(lesson)

            return redirect("lessons:lesson_list")

    else:

        form = LessonForm(instance=lesson)

    return render(request, "edit_lesson.html", {
        "form": form,
        "lesson": lesson,
    })


# ===================================
# LESSON PROGRESS
# ===================================

@login_required
def lesson_progress(request):

    progress = (
        LessonProgress.objects
        .filter(student=request.user)
        .select_related(
            "lesson",
            "lesson__created_by"
        )
        .order_by("-updated_at")
    )

    return render(request, "lesson_progress.html", {
        "progress": progress,
        "today": timezone.localdate(),
        "now": timezone.localtime(),
    })
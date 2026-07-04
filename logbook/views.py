from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import FileResponse
from django.conf import settings

from django.conf import settings
from .onlyoffice import OnlyOfficeConfig

import json


import os

from .models import (
    StudentLogbook,
    LogbookEntry
)

from .forms import (
    StudentLogbookForm,
    LogbookEntryForm,
    LogbookReviewForm
)

from .services import generate_weekly_report_pdf


# ==========================================
# UPLOAD LOGBOOK (ONCE)
# ==========================================



# ==========================================
# UPLOAD LOGBOOK
# ==========================================

@login_required
def upload_logbook(request):

    if request.user.role != "STUDENT":
        return redirect("dashboard:router")

    logbook = StudentLogbook.objects.filter(
        student=request.user
    ).first()

    if request.method == "POST":

        form = StudentLogbookForm(
            request.POST,
            request.FILES,
            instance=logbook
        )

        if form.is_valid():

            uploaded = form.save(commit=False)
            uploaded.student = request.user
            uploaded.save()

            messages.success(
                request,
                "Your logbook has been uploaded successfully."
            )

            return redirect(
                "logbook:edit_logbook"
            )

    else:

        form = StudentLogbookForm(
            instance=logbook
        )

    return render(
        request,
        "upload_logbook.html",
        {
            "form": form,
            "logbook": logbook,
        }
    )


# ==========================================
# EDIT LOGBOOK
# ==========================================





@login_required
def edit_logbook(request):

    if request.user.role != "STUDENT":
        return redirect("dashboard:router")

    logbook = StudentLogbook.objects.filter(
        student=request.user
    ).first()

    if not logbook:

        messages.warning(
            request,
            "Please upload your university logbook first."
        )

        return redirect(
            "logbook:upload_logbook"
        )

    extension = (
        logbook.logbook_file.name.split(".")[-1].lower()
    )

    # Build absolute URLs using SITE_URL
    document_url = (
        f"{settings.SITE_URL}{logbook.logbook_file.url}"
    )

    callback_url = (
        f"{settings.SITE_URL}/logbook/callback/{logbook.id}/"
    )

    document = {

        "fileType": extension,

        "title": (
            logbook.logbook_file.name.split("/")[-1]
        ),

        "url": document_url,

        # Unique key so ONLYOFFICE knows when the document changes
        "key": (
            f"logbook-{logbook.id}-{int(logbook.updated_at.timestamp())}"
        ),

        "callback": callback_url,

    }

    editor = OnlyOfficeConfig.get_config(
        document,
        request.user
    )

    return render(
        request,
        "edit_logbook.html",
        {
            "logbook": logbook,
            "editor": editor,
            "editor_config": json.dumps(editor["config"]),
            "document_url": document_url,
        }
    )
# ==========================================
# CREATE DAILY ENTRY
# ==========================================

@login_required
def create_entry(request):

    if request.user.role != "STUDENT":

        messages.error(
            request,
            "Only students can create logbook entries."
        )

        return redirect(
            "dashboard:router"
        )

    logbook = StudentLogbook.objects.filter(
        student=request.user
    ).first()

    if not logbook:

        messages.warning(
            request,
            "Please upload your university logbook first."
        )

        return redirect(
            "logbook:upload_logbook"
        )

    if request.method == "POST":

        form = LogbookEntryForm(request.POST)

        if form.is_valid():

            entry = form.save(commit=False)

            entry.student = request.user

            entry.logbook = logbook

            entry.save()

            messages.success(
                request,
                "Daily activity saved successfully."
            )

            return redirect(
                "logbook:daily_entries"
            )

    else:

        form = LogbookEntryForm()

    return render(
        request,
        "create_entry.html",
        {
            "form": form,
            "logbook": logbook
        }
    )


# ==========================================
# DAILY ENTRIES
# ==========================================

@login_required
def daily_entries(request):

    if request.user.role == "STUDENT":

        entries = LogbookEntry.objects.filter(
            student=request.user
        ).select_related("logbook")

    else:

        entries = LogbookEntry.objects.select_related(
            "student",
            "logbook"
        )

    return render(
        request,
        "daily_entries.html",
        {
            "entries": entries
        }
    )

# ==========================================
# REVIEW STUDENT LOGBOOK
# ==========================================

# ==========================================
# REVIEW STUDENT LOGBOOK
# ==========================================
@login_required
def supervisor_review(request, pk):

    if request.user.role not in ["TRAINER", "SUPER_ADMIN"]:
        return redirect("dashboard:router")

    logbook = get_object_or_404(
        StudentLogbook.objects.select_related("student"),
        pk=pk
    )

    if request.method == "POST":

        form = LogbookReviewForm(
            request.POST,
            instance=logbook
        )

        if form.is_valid():

            review = form.save(commit=False)
            review.reviewed_by = request.user
            review.reviewed_at = timezone.now()
            review.save()

            messages.success(
                request,
                f"{logbook.student.get_full_name() or logbook.student.username}'s logbook has been reviewed successfully."
            )

            return redirect("logbook:report")

    else:

        form = LogbookReviewForm(instance=logbook)

    extension = logbook.logbook_file.name.split(".")[-1].lower()

    document = {
        "fileType": extension,
        "title": logbook.logbook_file.name.split("/")[-1],
        "url": f"{settings.SITE_URL}{logbook.logbook_file.url}",
        "key": f"review-{logbook.id}-{int(logbook.updated_at.timestamp())}",
        "callback": f"{settings.SITE_URL}/logbook/callback/{logbook.id}/",
    }

    editor = OnlyOfficeConfig.get_config(
        document,
        request.user
    )

    # Trainer should only review, not edit
    editor["config"]["editorConfig"]["mode"] = "view"
    editor["config"]["permissions"]["edit"] = False
    editor["config"]["permissions"]["review"] = False

    return render(
        request,
        "supervisor_review.html",
        {
            "logbook": logbook,
            "form": form,
            "editor": editor,
            "editor_config": json.dumps(editor["config"]),
        }
    )
# ==========================================
# MONTHLY SUMMARY
# ==========================================

@login_required
def monthly_summary(request):

    logbook = StudentLogbook.objects.filter(
        student=request.user
    ).first()

    return render(
        request,
        "monthly_summary.html",
        {
            "logbook": logbook,
        }
    )

# ==========================================
# ADMIN REPORT
# ==========================================
@login_required
def logbook_report(request):

    if request.user.role not in [
        "SUPER_ADMIN",
        "TRAINER"
    ]:
        return redirect("dashboard:router")

    logbooks = StudentLogbook.objects.select_related(
        "student",
        "reviewed_by"
    )

    return render(
        request,
        "logbook_report.html",
        {
            "logbooks": logbooks,
        }
    )


# ==========================================
# DOWNLOAD WEEKLY REPORT
# ==========================================

@login_required
def download_weekly_report(request):

    if request.user.role != "STUDENT":

        return redirect(
            "dashboard:router"
        )

    file_path = os.path.join(
        settings.MEDIA_ROOT,
        f"weekly_{request.user.id}.pdf"
    )

    generate_weekly_report_pdf(
        request.user,
        file_path
    )

    return FileResponse(
        open(file_path, "rb"),
        content_type="application/pdf"
    )

# ==========================================
# VIEW STUDENT LOGBOOK (TRAINER / ADMIN)
# ==========================================

@login_required
def view_logbook(request, pk):

    if request.user.role not in [
        "TRAINER",
        "SUPER_ADMIN",
    ]:
        return redirect("dashboard:router")

    logbook = get_object_or_404(
        StudentLogbook.objects.select_related("student"),
        pk=pk
    )

    extension = (
        logbook.logbook_file.name
        .split(".")[-1]
        .lower()
    )

    document = {

        "fileType": extension,

        "title": (
            logbook.logbook_file.name.split("/")[-1]
        ),

        "url": (
            f"{settings.SITE_URL}"
            f"{logbook.logbook_file.url}"
        ),

        "key": (
            f"logbook-{logbook.id}-"
            f"{int(logbook.updated_at.timestamp())}"
        ),

        "callback": (
            f"{settings.SITE_URL}"
            f"/logbook/callback/{logbook.id}/"
        ),

    }

    editor = OnlyOfficeConfig.get_config(
        document,
        request.user
    )

    # Open document in VIEW mode
    editor["config"]["editorConfig"]["mode"] = "view"

    return render(
        request,
        "view_logbook.html",
        {
            "logbook": logbook,
            "editor": editor,
            "editor_config": json.dumps(
                editor["config"]
            ),
        }
    )

# ==========================================
# SUBMIT LOGBOOK FOR REVIEW
# ==========================================

@login_required
def submit_logbook(request, pk):

    if request.user.role != "STUDENT":
        return redirect("dashboard:router")

    logbook = get_object_or_404(
        StudentLogbook,
        pk=pk,
        student=request.user
    )

    if request.method == "POST":

        # Student submits latest edited version
        logbook.status = "PENDING"

        # Clear previous review information
        logbook.reviewed_by = None
        logbook.reviewed_at = None
        logbook.remarks = ""

        logbook.save()

        messages.success(
            request,
            "Your logbook has been submitted for review successfully."
        )

    return redirect("logbook:edit_logbook")
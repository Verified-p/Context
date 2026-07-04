from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import uuid
from django.contrib import messages



from .forms import AssignmentForm

from .models import (
    Assignment,
    AssignmentSubmission
)

from .forms import (
    AssignmentForm,
    AssignmentSubmissionForm,
    GradeSubmissionForm
)

from .services import (
    assignment_statistics,
    grade_submission
)





@login_required
def assignment_list(request):

    user = request.user

    # Trainers + Admin see everything
    if user.role in ["SUPER_ADMIN", "TRAINER"]:
        assignments = Assignment.objects.all().order_by("-created_at")

    # Students ONLY see published
    else:
        assignments = Assignment.objects.filter(
            status="PUBLISHED"
        ).order_by("-created_at")

    return render(request, "assignment_list.html", {
        "assignments": assignments
    })

# =====================================================
# ASSIGNMENT DETAIL
# =====================================================

@login_required
def assignment_detail(request, pk):

    assignment = get_object_or_404(
        Assignment,
        pk=pk
    )

    stats = assignment_statistics(
        assignment
    )

    context = {
        "assignment": assignment,
        "stats": stats
    }

    return render(
        request,
        "assignment_detail.html",
        context
    )


# =====================================================
# CREATE ASSIGNMENT
# =====================================================




@login_required
def create_assignment(request):

    # =========================
    # PERMISSION CHECK
    # =========================
    if request.user.role not in ["SUPER_ADMIN", "TRAINER"]:
        messages.error(request, "Permission denied.")
        return redirect("dashboard:router")

    # =========================
    # POST REQUEST
    # =========================
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)

        if form.is_valid():
            assignment = form.save(commit=False)

            # 🔥 REQUIRED FIXES
            assignment.created_by = request.user

            # auto-generate assignment code
            assignment.assignment_code = str(uuid.uuid4())[:8].upper()

            # default status
            assignment.status = "DRAFT"

            assignment.save()

            messages.success(request, "Assignment created successfully.")
            return redirect("assignments:list")

        else:
            # show errors clearly
            messages.error(request, "Please correct the errors below.")
            print("FORM ERRORS:", form.errors)

    # =========================
    # GET REQUEST
    # =========================
    else:
        form = AssignmentForm()

    return render(request, "create_assignment.html", {
        "form": form
    })


# =====================================================
# EDIT ASSIGNMENT
# =====================================================

@login_required
def edit_assignment(request, pk):

    assignment = get_object_or_404(
        Assignment,
        pk=pk
    )

    if request.user.role not in [
        "SUPER_ADMIN",
        "TRAINER"
    ]:

        messages.error(
            request,
            "Permission denied."
        )

        return redirect(
            "dashboard:router"
        )

    if request.method == "POST":

        form = AssignmentForm(
            request.POST,
            request.FILES,
            instance=assignment
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Assignment updated successfully."
            )

            return redirect(
                "assignments:list"
            )

    else:

        form = AssignmentForm(
            instance=assignment
        )

    context = {
        "form": form,
        "assignment": assignment
    }

    return render(
        request,
        "create_assignment.html",
        context
    )


# =====================================================
# SUBMIT ASSIGNMENT
# =====================================================

@login_required
def submit_assignment(request, pk):

    assignment = get_object_or_404(
        Assignment,
        pk=pk
    )

    if request.user.role != "STUDENT":

        messages.error(
            request,
            "Only students can submit assignments."
        )

        return redirect(
            "assignments:list"
        )

    existing_submission = AssignmentSubmission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()

    if existing_submission:

        messages.warning(
            request,
            "You already submitted this assignment."
        )

        return redirect(
            "assignments:list"
        )

    if request.method == "POST":

        form = AssignmentSubmissionForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            submission = form.save(
                commit=False
            )

            submission.assignment = assignment
            submission.student = request.user

            submission.save()

            messages.success(
                request,
                "Assignment submitted successfully."
            )

            return redirect(
                "assignments:list"
            )

    else:

        form = AssignmentSubmissionForm()

    context = {
        "form": form,
        "assignment": assignment
    }

    return render(
        request,
        "submit_assignment.html",
        context
    )


# =====================================================
# SUBMISSIONS
# =====================================================

@login_required
def submissions(request):

    if request.user.role in [
        "SUPER_ADMIN",
        "TRAINER"
    ]:

        submissions = AssignmentSubmission.objects.select_related(
            "assignment",
            "student"
        )

    else:

        submissions = AssignmentSubmission.objects.filter(
            student=request.user
        )

    context = {
        "submissions": submissions
    }

    return render(
        request,
        "submissions.html",
        context
    )


# =====================================================
# GRADE SUBMISSION
# =====================================================

@login_required
def grading(request, pk):

    submission = get_object_or_404(
        AssignmentSubmission,
        pk=pk
    )

    if request.user.role not in [
        "SUPER_ADMIN",
        "TRAINER"
    ]:

        messages.error(
            request,
            "Permission denied."
        )

        return redirect(
            "assignments:submissions"
        )

    if request.method == "POST":

        form = GradeSubmissionForm(
            request.POST,
            instance=submission
        )

        if form.is_valid():

            grade_submission(
                submission=submission,
                marks=form.cleaned_data["marks_awarded"],
                feedback=form.cleaned_data["feedback"],
                grader=request.user
            )

            messages.success(
                request,
                "Assignment graded successfully."
            )

            return redirect(
                "assignments:submissions"
            )

    else:

        form = GradeSubmissionForm(
            instance=submission
        )

    context = {
        "form": form,
        "submission": submission
    }

    return render(
        request,
        "grading.html",
        context
    )


# =====================================================
# FEEDBACK
# =====================================================

@login_required
def feedback(request, pk):

    submission = get_object_or_404(
        AssignmentSubmission,
        pk=pk
    )

    context = {
        "submission": submission
    }

    return render(
        request,
        "feedback.html",
        context
    )





@login_required
def publish_assignment(request, pk):

    if request.user.role not in ["SUPER_ADMIN", "TRAINER"]:
        messages.error(request, "Permission denied.")
        return redirect("assignments:list")

    assignment = get_object_or_404(Assignment, pk=pk)

    assignment.status = "PUBLISHED"
    assignment.save()

    messages.success(request, "Assignment published successfully.")

    return redirect("assignments:list")
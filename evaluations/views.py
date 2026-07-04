from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Evaluation
from .forms import EvaluationForm
from .services import calculate_student_average



from students.models import Student
from .services import EvaluationAnalyticsService


from .services import (
    get_top_students,
    get_weak_students,
)

from .services import get_evaluation_trends
# =========================
# LIST
# =========================
@login_required
def evaluation_list(request):

    if request.user.role in ["SUPER_ADMIN", "TRAINER"]:
        evaluations = Evaluation.objects.all()
    else:
        evaluations = Evaluation.objects.filter(student=request.user)

    return render(request, "evaluation_list.html", {
        "evaluations": evaluations
    })


# =========================
# CREATE / EVALUATE
# =========================
@login_required
def evaluate_student(request):

    if request.user.role not in ["SUPER_ADMIN", "TRAINER"]:
        messages.error(request, "Permission denied.")
        return redirect("dashboard:router")

    if request.method == "POST":
        form = EvaluationForm(request.POST)

        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.trainer = request.user
            evaluation.save()

            messages.success(request, "Evaluation saved successfully.")
            return redirect("evaluations:list")

    else:
        form = EvaluationForm()

    return render(request, "evaluate_student.html", {
        "form": form
    })


# =========================
# REPORT
# =========================
@login_required
def evaluation_report(request, pk):

    evaluation = get_object_or_404(Evaluation, pk=pk)

    return render(request, "evaluation_report.html", {
        "evaluation": evaluation
    })


# =========================
# SUMMARY
# =========================


@login_required
def evaluation_summary(request):

    avg = calculate_student_average(request.user)
    data = get_evaluation_trends(request.user)

    return render(
        request,
        "evaluation_summary.html",
        {
            "avg": avg,
            "data": data,
        }
    )




@login_required
def analytics(request):

    if request.user.role not in [
        "TRAINER",
        "SUPER_ADMIN"
    ]:
        return redirect(
            "dashboard:router"
        )

    top_students = get_top_students()
    weak_students = get_weak_students()

    context = {
        "top_students": top_students,
        "weak_students": weak_students,
    }

    return render(
        request,
        "evaluation_analytics.html",
        context
    )






@login_required
def evaluation_dashboard(request):

    if request.user.role not in ["TRAINER", "SUPER_ADMIN"]:
        return render(request, "403.html")

    students = Student.objects.all()

    top_students = EvaluationAnalyticsService.get_top_students(students)
    at_risk_students = EvaluationAnalyticsService.get_at_risk_students(students)

    context = {
        "top_students": top_students,
        "at_risk_students": at_risk_students,
    }

    return render(request, "evaluation_summary.html", context)
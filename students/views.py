from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Student
from .forms import StudentRegistrationForm
from accounts.models import User


# ==========================================
# REGISTER STUDENT (ADMIN ONLY)
# ==========================================

@login_required
def register_student(request):

    if request.user.role != "SUPER_ADMIN":

        messages.error(
            request,
            "Only administrators can register students."
        )

        return redirect(
            "students:list"
        )

    if request.method == "POST":

        form = StudentRegistrationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            admission_number = form.cleaned_data[
                "admission_number"
            ]

            national_id = form.cleaned_data[
                "national_id"
            ]

            email = form.cleaned_data[
                "email"
            ]

            full_name = form.cleaned_data[
                "full_name"
            ]

            if User.objects.filter(
                username=admission_number
            ).exists():

                messages.error(
                    request,
                    "A user with this admission number already exists."
                )

                return render(
                    request,
                    "registration.html",
                    {
                        "form": form
                    }
                )

            names = full_name.split()

            first_name = names[0]

            last_name = (
                " ".join(names[1:])
                if len(names) > 1
                else ""
            )

            user = User.objects.create_user(
                username=admission_number,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role="STUDENT",
                is_active=True
            )

            user.set_password(
                national_id
            )

            user.save()

            student = form.save(
                commit=False
            )

            student.user = user
            student.status = "PENDING"

            student.save()

            messages.success(
                request,
                (
                    f"Student registered successfully. "
                    f"Username: {admission_number} | "
                    f"Password: {national_id}"
                )
            )

            return redirect(
                "students:list"
            )

    else:

        form = StudentRegistrationForm()

    return render(
        request,
        "registration.html",
        {
            "form": form
        }
    )


# ==========================================
# PUBLIC STUDENT REGISTRATION
# ==========================================

def student_register(request):

    if request.user.is_authenticated:
        return redirect("students:dashboard")

    if request.method == "POST":

        form = StudentRegistrationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            admission_number = form.cleaned_data["admission_number"]
            national_id = form.cleaned_data["national_id"]
            email = form.cleaned_data["email"]
            full_name = form.cleaned_data["full_name"]

            names = full_name.split()

            first_name = names[0]

            last_name = (
                " ".join(names[1:])
                if len(names) > 1
                else ""
            )

            user = User.objects.create_user(
                username=admission_number,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role="STUDENT",
                is_active=False
            )

            user.set_password(national_id)
            user.save()

            student = form.save(commit=False)

            student.user = user
            student.status = "PENDING"

            student.save()

            messages.success(
                request,
                (
                    "Registration submitted successfully. "
                    "Please wait for administrator approval. "
                    "After approval, log in using your "
                    "Admission Number as the username and "
                    "National ID as the password."
                )
            )

            return redirect("accounts:login")

    else:

        form = StudentRegistrationForm()

    return render(
        request,
        "student_register.html",
        {
            "form": form
        }
    )


# ==========================================
# STUDENT DASHBOARD
# ==========================================

@login_required
def student_dashboard(request):

    student = Student.objects.filter(
        user=request.user
    ).first()

    return render(
        request,
        "student_dashboard.html",
        {
            "student": student
        }
    )


# ==========================================
# STUDENT PROFILE
# ==========================================

@login_required
def student_profile(request):

    student = Student.objects.filter(
        user=request.user
    ).first()

    return render(
        request,
        "student_profile.html",
        {
            "student": student
        }
    )


# ==========================================
# ALL STUDENTS
# ==========================================

@login_required
def student_list(request):

    students = Student.objects.select_related(
        "user"
    ).all()

    return render(
        request,
        "student_list.html",
        {
            "students": students
        }
    )


# ==========================================
# STUDENT DETAIL
# ==========================================

@login_required
def student_detail(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    return render(
        request,
        "student_detail.html",
        {
            "student": student
        }
    )


# ==========================================
# PENDING APPROVALS
# ==========================================

@login_required
def pending_approvals(request):

    students = Student.objects.filter(
        status="PENDING"
    )

    return render(
        request,
        "pending_approvals.html",
        {
            "students": students
        }
    )


# ==========================================
# APPROVED STUDENTS
# ==========================================

@login_required
def approved_students(request):

    students = Student.objects.filter(
        status="APPROVED"
    )

    return render(
        request,
        "approved_students.html",
        {
            "students": students
        }
    )


# ==========================================
# APPROVE STUDENT
# ==========================================

@login_required
def approve_student_view(request, pk):

    if request.user.role != "SUPER_ADMIN":

        messages.error(
            request,
            "Only administrators can approve students."
        )

        return redirect(
            "students:pending_approvals"
        )

    student = get_object_or_404(
        Student,
        pk=pk
    )

    student.status = "APPROVED"
    student.approved_by = request.user
    student.approved_at = timezone.now()

    student.save()

    if student.user:

        student.user.is_active = True
        student.user.is_verified = True
        student.user.save()

    messages.success(
        request,
        (
            f"{student.full_name} approved successfully. "
            f"Login Username: {student.admission_number}"
        )
    )

    return redirect(
        "students:pending_approvals"
    )


# ==========================================
# REJECT STUDENT
# ==========================================

@login_required
def reject_student_view(request, pk):

    if request.user.role != "SUPER_ADMIN":

        messages.error(
            request,
            "Only administrators can reject students."
        )

        return redirect(
            "students:pending_approvals"
        )

    student = get_object_or_404(
        Student,
        pk=pk
    )

    student.status = "REJECTED"

    student.save()

    if student.user:

       student.user.is_active = False
       student.user.is_verified = False
       student.user.save()

    messages.warning(
        request,
        f"{student.full_name} has been rejected."
    )

    return redirect(
        "students:pending_approvals"
    )
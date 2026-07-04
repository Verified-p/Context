# accounts/views.py

from django.contrib import messages
from django.contrib.auth import (
    login,
    logout,
    authenticate,
    update_session_auth_hash
)

from django.contrib.auth.decorators import login_required

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import User

from .forms import (
    LoginForm,
    UserCreateForm,
    ProfileUpdateForm,
    CustomPasswordChangeForm
)

from .services import (
    UserService,
    AuditService
)

from .permissions import (
    super_admin_required
)


# ==========================================
# LOGIN
# ==========================================

def login_view(request):

    if request.user.is_authenticated:

        if request.user.role == "STUDENT":
            return redirect("students:dashboard")

        return redirect("accounts:profile")

    form = LoginForm(
        request,
        data=request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data.get(
                "username"
            )

            password = form.cleaned_data.get(
                "password"
            )

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:

                if user.is_locked:

                    messages.error(
                        request,
                        "Your account has been locked."
                    )

                    return redirect(
                        "accounts:login"
                    )

                login(
                    request,
                    user
                )

                if not form.cleaned_data.get(
                    "remember_me"
                ):
                    request.session.set_expiry(0)

                messages.success(
                    request,
                    f"Welcome {user.first_name or user.username}"
                )

                # ==========================
                # ROLE BASED REDIRECTS
                # ==========================

                if user.role == "SUPER_ADMIN":
                    return redirect(
                        "accounts:profile"
                    )

                elif user.role == "TRAINER":
                    return redirect(
                        "accounts:profile"
                    )

                elif user.role == "FINANCE":
                    return redirect(
                        "accounts:profile"
                    )

                elif user.role == "STUDENT":
                    return redirect(
                        "students:dashboard"
                    )

                return redirect(
                    "accounts:profile"
                )

    return render(
        request,
        "login.html",
        {
            "form": form
        }
    )


# ==========================================
# LOGOUT
# ==========================================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect(
        "accounts:login"
    )


# ==========================================
# PROFILE
# ==========================================

@login_required
def profile_view(request):

    if request.method == "POST":

        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect(
                "accounts:profile"
            )

    else:

        form = ProfileUpdateForm(
            instance=request.user
        )

    return render(
        request,
        "profile.html",
        {
            "form": form,
            "user_obj": request.user
        }
    )


# ==========================================
# CHANGE PASSWORD
# ==========================================

@login_required
def change_password(request):

    if request.method == "POST":

        form = CustomPasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Password changed successfully."
            )

            return redirect(
                "accounts:profile"
            )

    else:

        form = CustomPasswordChangeForm(
            request.user
        )

    return render(
        request,
        "change_password.html",
        {
            "form": form
        }
    )


# ==========================================
# USER LIST
# ==========================================

@login_required
@super_admin_required
def user_list(request):

    users = User.objects.all().order_by(
        "-date_joined"
    )

    return render(
        request,
        "user_list.html",
        {
            "users": users
        }
    )


# ==========================================
# CREATE USER
# ==========================================

@login_required
@super_admin_required
def create_user(request):

    if request.method == "POST":

        form = UserCreateForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            user = UserService.create_user(
                form
            )

            AuditService.log(
                request.user,
                "CREATE",
                f"Created user {user.username}"
            )

            messages.success(
                request,
                f"{user.get_full_name() or user.username} created successfully."
            )

            return redirect(
                "accounts:user_list"
            )

    else:

        form = UserCreateForm()

    return render(
        request,
        "create_user.html",
        {
            "form": form
        }
    )


# ==========================================
# ACTIVATE USER
# ==========================================

@login_required
@super_admin_required
def activate_user(request, user_id):

    user = get_object_or_404(
        User,
        pk=user_id
    )

    UserService.activate_user(
        user
    )

    AuditService.log(
        request.user,
        "UPDATE",
        f"Activated user {user.username}"
    )

    messages.success(
        request,
        "User activated successfully."
    )

    return redirect(
        "accounts:user_list"
    )


# ==========================================
# DEACTIVATE USER
# ==========================================

@login_required
@super_admin_required
def deactivate_user(request, user_id):

    user = get_object_or_404(
        User,
        pk=user_id
    )

    UserService.deactivate_user(
        user
    )

    AuditService.log(
        request.user,
        "UPDATE",
        f"Deactivated user {user.username}"
    )

    messages.success(
        request,
        "User deactivated successfully."
    )

    return redirect(
        "accounts:user_list"
    )


# ==========================================
# UNLOCK USER
# ==========================================

@login_required
@super_admin_required
def unlock_user(request, user_id):

    user = get_object_or_404(
        User,
        pk=user_id
    )

    UserService.unlock_user(
        user
    )

    AuditService.log(
        request.user,
        "UPDATE",
        f"Unlocked user {user.username}"
    )

    messages.success(
        request,
        "Account unlocked successfully."
    )

    return redirect(
        "accounts:user_list"
    )

# ==========================================
# USER DETAIL
# ==========================================

@login_required
@super_admin_required
def user_detail(request, user_id):

    user = get_object_or_404(
        User,
        pk=user_id
    )

    return render(
        request,
        "user_detail.html",
        {
            "selected_user": user
        }
    )


# ==========================================
# RESET USER PASSWORD
# ==========================================

@login_required
@super_admin_required
def reset_user_password(request, user_id):

    user = get_object_or_404(
        User,
        pk=user_id
    )

    # Default password
    default_password = "12345678"

    user.set_password(
        default_password
    )

    user.save()

    messages.success(
        request,
        f"Password for {user.username} has been reset to {default_password}"
    )

    return redirect(
        "accounts:user_list"
    )


# ==========================================
# DELETE USER
# ==========================================

@login_required
@super_admin_required
def delete_user(request, user_id):

    user = get_object_or_404(
        User,
        pk=user_id
    )

    username = user.username

    user.delete()

    messages.success(
        request,
        f"User {username} deleted successfully."
    )

    return redirect(
        "accounts:user_list"
    )
# accounts/urls.py

from django.urls import path


from .views import (
    login_view,
    logout_view,
    profile_view,
    change_password,
    user_list,
    create_user,
    activate_user,
    deactivate_user,
    unlock_user,

    # New views
    user_detail,
    delete_user,
    reset_user_password,
)

app_name = "accounts"

urlpatterns = [

    # ==========================================
    # AUTHENTICATION
    # ==========================================

    path(
        "login/",
        login_view,
        name="login"
    ),
 

    path(
        "logout/",
        logout_view,
        name="logout"
    ),

    # ==========================================
    # PROFILE
    # ==========================================

    path(
        "profile/",
        profile_view,
        name="profile"
    ),

    path(
        "change-password/",
        change_password,
        name="change_password"
    ),

    # ==========================================
    # USER MANAGEMENT
    # ==========================================

    path(
        "users/",
        user_list,
        name="user_list"
    ),

    path(
        "users/create/",
        create_user,
        name="create_user"
    ),

    path(
        "users/<int:user_id>/",
        user_detail,
        name="user_detail"
    ),

    path(
        "users/<int:user_id>/activate/",
        activate_user,
        name="activate_user"
    ),

    path(
        "users/<int:user_id>/deactivate/",
        deactivate_user,
        name="deactivate_user"
    ),

    path(
        "users/<int:user_id>/unlock/",
        unlock_user,
        name="unlock_user"
    ),

    path(
        "users/<int:user_id>/reset-password/",
        reset_user_password,
        name="reset_password"
    ),

    path(
        "users/<int:user_id>/delete/",
        delete_user,
        name="delete_user"
    ),

    
]
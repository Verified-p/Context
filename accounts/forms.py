# accounts/forms.py

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm
)

from .models import User


# ==========================================
# LOGIN FORM
# ==========================================

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Admission Number or Username"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password"
            }
        )
    )

    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input"
            }
        )
    )


# ==========================================
# CREATE USER FORM
# (TRAINERS / FINANCE ONLY)
# ==========================================

class UserCreateForm(forms.ModelForm):

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:

        model = User

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "role",
            "profile_picture",
            "password",
        ]

        widgets = {

            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "username": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),

            "phone_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "role": forms.Select(
                attrs={"class": "form-select"}
            ),

            "profile_picture": forms.FileInput(
                attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Students must come from Students module

        self.fields["role"].choices = [
            ("TRAINER", "Trainer"),
            ("FINANCE", "Finance Officer"),
            ("SUPER_ADMIN", "Super Admin"),
        ]

    # ==========================================
    # EMAIL VALIDATION
    # ==========================================

    def clean_email(self):

        email = self.cleaned_data.get(
            "email"
        )

        if User.objects.filter(
            email=email
        ).exists():

            raise forms.ValidationError(
                "Email already exists."
            )

        return email

    # ==========================================
    # USERNAME VALIDATION
    # ==========================================

    def clean_username(self):

        username = self.cleaned_data.get(
            "username"
        )

        if User.objects.filter(
            username=username
        ).exists():

            raise forms.ValidationError(
                "Username already exists."
            )

        return username

    # ==========================================
    # PASSWORD MATCH
    # ==========================================

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            "password"
        )

        confirm_password = cleaned_data.get(
            "confirm_password"
        )

        if (
            password and
            confirm_password and
            password != confirm_password
        ):

            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data

    # ==========================================
    # SAVE USER
    # ==========================================

    def save(self, commit=True):

        user = super().save(
            commit=False
        )

        user.set_password(
            self.cleaned_data["password"]
        )

        if commit:
            user.save()

        return user


# ==========================================
# PROFILE UPDATE FORM
# ==========================================

class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "profile_picture",
        ]

        widgets = {

            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),

            "phone_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "profile_picture": forms.FileInput(
                attrs={"class": "form-control"}
            ),
        }

    def clean_email(self):

        email = self.cleaned_data.get(
            "email"
        )

        existing = User.objects.filter(
            email=email
        ).exclude(
            pk=self.instance.pk
        )

        if existing.exists():

            raise forms.ValidationError(
                "Email already in use."
            )

        return email


# ==========================================
# CHANGE PASSWORD FORM
# ==========================================

class CustomPasswordChangeForm(
    PasswordChangeForm
):

    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
from django import forms

from .models import Student
from accounts.models import User


class StudentRegistrationForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [

            # ==========================
            # PERSONAL INFORMATION
            # ==========================
            "full_name",
            "admission_number",
            "national_id",
            "gender",
            "date_of_birth",
            "phone_number",
            "email",
            "county",
            "sub_county",
            "physical_address",

            # ==========================
            # INSTITUTION DETAILS
            # ==========================
            "institution",
            "department",
            "course",
            "year_of_study",
            "duration",
            "start_date",
            "end_date",
            "training_mode",
            "session",

            # ==========================
            # EMERGENCY CONTACT
            # ==========================
            "emergency_contact_name",
            "emergency_contact_phone",

            # ==========================
            # DOCUMENTS
            # ==========================
            "passport_photo",
            "id_copy",
            "introduction_letter",
        ]

        widgets = {

            "full_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "admission_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "national_id": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "gender": forms.Select(
                attrs={"class": "form-select"}
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "phone_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),

            "county": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "sub_county": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "physical_address": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                }
            ),

            "institution": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "department": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "course": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "year_of_study": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "duration": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "training_mode": forms.Select(
                attrs={"class": "form-select"}
            ),

            "session": forms.Select(
                attrs={"class": "form-select"}
            ),

            "emergency_contact_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "emergency_contact_phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "passport_photo": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),

            "id_copy": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),

            "introduction_letter": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }

    # ==========================================
    # VALIDATION
    # ==========================================

    def clean_admission_number(self):

        admission_number = self.cleaned_data["admission_number"]

        if Student.objects.filter(
            admission_number=admission_number
        ).exists():

            raise forms.ValidationError(
                "This admission number is already registered."
            )

        if User.objects.filter(
            username=admission_number
        ).exists():

            raise forms.ValidationError(
                "This admission number is already in use."
            )

        return admission_number

    def clean_national_id(self):

        national_id = self.cleaned_data["national_id"]

        if Student.objects.filter(
            national_id=national_id
        ).exists():

            raise forms.ValidationError(
                "This National ID already exists."
            )

        return national_id

    def clean_email(self):

        email = self.cleaned_data["email"]

        if Student.objects.filter(
            email=email
        ).exists():

            raise forms.ValidationError(
                "This email is already registered."
            )

        if User.objects.filter(
            email=email
        ).exists():

            raise forms.ValidationError(
                "This email is already associated with another account."
            )

        return email

    def clean_phone_number(self):

        phone = self.cleaned_data["phone_number"]

        if Student.objects.filter(
            phone_number=phone
        ).exists():

            raise forms.ValidationError(
                "This phone number is already registered."
            )

        return phone

    def clean(self):

        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if (
            start_date
            and end_date
            and end_date < start_date
        ):

            raise forms.ValidationError(
                "End date cannot be earlier than the start date."
            )

        return cleaned_data
from django import forms

from .models import (
    StudentLogbook,
    LogbookEntry
)


# ==========================================
# UPLOAD UNIVERSITY LOGBOOK
# ==========================================


# ==========================================
# STUDENT UPLOAD FORM
# ==========================================

class StudentLogbookForm(forms.ModelForm):

    class Meta:

        model = StudentLogbook

        fields = [
            "logbook_file",
        ]

        widgets = {

            "logbook_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            )

        }




# ==========================================
# DAILY LOGBOOK ENTRY
# ==========================================

class LogbookEntryForm(forms.ModelForm):

    class Meta:
        model = LogbookEntry

        fields = [
            "title",
            "activity",
            "reflection",
            "date",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Network Installation"
                }
            ),

            "activity": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe the activities you carried out today..."
                }
            ),

            "reflection": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "What did you learn today? (Optional)"
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),
        }


# ==========================================
# TRAINER REVIEW FORM
# ==========================================

class LogbookReviewForm(forms.ModelForm):

    class Meta:

        model = StudentLogbook

        fields = [
            "status",
            "remarks",
        ]

        widgets = {

            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter remarks for the student..."
                }
            ),

        }



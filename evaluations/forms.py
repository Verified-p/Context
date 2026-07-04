from django import forms
from .models import Evaluation


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            "student",
            "lesson",
            "title",
            "technical_score",
            "discipline_score",
            "attendance_score",
            "communication_score",
            "feedback",
            "period_start",
            "period_end",
            "status",
        ]

        widgets = {
            "student": forms.Select(attrs={"class": "form-select"}),
            "lesson": forms.Select(attrs={"class": "form-select"}),

            "title": forms.TextInput(attrs={"class": "form-control"}),

            "technical_score": forms.NumberInput(attrs={"class": "form-control"}),
            "discipline_score": forms.NumberInput(attrs={"class": "form-control"}),
            "attendance_score": forms.NumberInput(attrs={"class": "form-control"}),
            "communication_score": forms.NumberInput(attrs={"class": "form-control"}),

            "feedback": forms.Textarea(attrs={"class": "form-control", "rows": 4}),

            "period_start": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "period_end": forms.DateInput(attrs={"type": "date", "class": "form-control"}),

            "status": forms.Select(attrs={"class": "form-select"}),
        }
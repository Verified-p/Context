from django import forms
from .models import TrainerProfile


class TrainerProfileForm(forms.ModelForm):

    class Meta:
        model = TrainerProfile
        fields = ["full_name", "phone", "specialization", "bio"]

        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "specialization": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
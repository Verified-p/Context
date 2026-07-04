from django import forms
from django.utils import timezone
from .models import AttendanceSession


class AttendanceSessionForm(forms.ModelForm):

    class Meta:
        model = AttendanceSession

        fields = [
            "title",
            "course",
            "opens_at",
            "duration_minutes",
            "is_active",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Attendance Title"
                }
            ),

            "course": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Course or Unit"
                }
            ),

            "opens_at": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),

            "duration_minutes": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 180,
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["opens_at"].input_formats = [
            "%Y-%m-%dT%H:%M"
        ]

        if not self.instance.pk:

            now = timezone.localtime().replace(
                second=0,
                microsecond=0
            )

            self.fields["opens_at"].initial = now.strftime(
                "%Y-%m-%dT%H:%M"
            )

            self.fields["duration_minutes"].initial = 20

            self.fields["is_active"].initial = True

    def clean_duration_minutes(self):

        duration = self.cleaned_data.get("duration_minutes")

        if duration is None:
            raise forms.ValidationError(
                "Please enter the attendance duration."
            )

        if duration < 1:
            raise forms.ValidationError(
                "Duration must be at least 1 minute."
            )

        if duration > 180:
            raise forms.ValidationError(
                "Duration cannot exceed 180 minutes."
            )

        return duration

    def clean(self):

        cleaned_data = super().clean()

        opens_at = cleaned_data.get("opens_at")

        if opens_at:

            if timezone.is_naive(opens_at):
                opens_at = timezone.make_aware(
                    opens_at,
                    timezone.get_current_timezone()
                )

            cleaned_data["opens_at"] = opens_at

        return cleaned_data
from django import forms
from .models import Lesson


class LessonForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = [
            "title",
            "lesson_code",
            "description",

            "lesson_type",

            # Recorded Lesson
            "video",
            "pdf",
            "recording",

            # Live Lesson
            "lesson_date",
            "start_time",
            "end_time",
            "meeting_link",

            "status",
        ]

        widgets = {

            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Lesson Title"
            }),

            "lesson_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. CS101"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5
            }),

            "lesson_type": forms.Select(attrs={
                "class": "form-select"
            }),

            "video": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "pdf": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "recording": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "lesson_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),

            "start_time": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-control"
            }),

            "end_time": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-control"
            }),

            "meeting_link": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://meet.google.com/..."
            }),

            "status": forms.Select(attrs={
                "class": "form-select"
            }),
        }

    def clean(self):

        cleaned_data = super().clean()

        lesson_type = cleaned_data.get("lesson_type")

        video = cleaned_data.get("video")
        recording = cleaned_data.get("recording")

        meeting_link = cleaned_data.get("meeting_link")
        lesson_date = cleaned_data.get("lesson_date")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        # ============================
        # RECORDED LESSON VALIDATION
        # ============================

        if lesson_type == "RECORDED":

            if not video and not recording:

                raise forms.ValidationError(
                    "Upload a lesson video or a recorded lesson."
                )

        # ============================
        # LIVE LESSON VALIDATION
        # ============================

        if lesson_type == "LIVE":

            if not lesson_date:
                self.add_error(
                    "lesson_date",
                    "Please select the lesson date."
                )

            if not start_time:
                self.add_error(
                    "start_time",
                    "Please select the lesson start time."
                )

            if not end_time:
                self.add_error(
                    "end_time",
                    "Please select the lesson end time."
                )

            if not meeting_link:
                self.add_error(
                    "meeting_link",
                    "Please provide the Google Meet or Zoom link."
                )

            if start_time and end_time:

                if end_time <= start_time:

                    self.add_error(
                        "end_time",
                        "End time must be later than the start time."
                    )

        return cleaned_data
from django import forms
from .models import Assignment, AssignmentSubmission



class AssignmentForm(forms.ModelForm):
    """
    Create/Edit Assignment
    """

    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Assignment

        fields = [
            'title',
            'lesson',
            'instructions',
            'attachment',
            'total_marks',
            'due_date'
        ]  # ❗ removed assignment_code + status

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'lesson': forms.Select(attrs={'class': 'form-select'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AssignmentSubmissionForm(forms.ModelForm):
    """
    Student Submission Form
    """

    class Meta:
        model = AssignmentSubmission
        fields = ['submission_file']

        widgets = {
            'submission_file': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            )
        }

    def clean_submission_file(self):
        file = self.cleaned_data.get('submission_file')

        if not file:
            raise forms.ValidationError("Please upload your assignment file.")

        allowed_extensions = ['.pdf', '.doc', '.docx', '.zip', '.jpg', '.jpeg', '.png']

        filename = file.name.lower()

        if not any(filename.endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError(
                "Only PDF, DOC, DOCX, ZIP and Image files are allowed."
            )

        return file


class GradeSubmissionForm(forms.ModelForm):
    """
    Trainer Grading Form
    """

    class Meta:
        model = AssignmentSubmission
        fields = ['marks_awarded', 'feedback']

        widgets = {
            'marks_awarded': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),

            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            })
        }

    def clean_marks_awarded(self):
        marks = self.cleaned_data.get('marks_awarded')

        if marks is not None and marks < 0:
            raise forms.ValidationError("Marks cannot be negative.")

        return marks
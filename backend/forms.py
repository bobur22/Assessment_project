from django import forms
from .models import TaskSubmission


class TaskSubmissionForm(forms.ModelForm):
    class Meta:
        model = TaskSubmission
        fields = ['task_type', 'maqola', 'tezis']
        widgets = {
            'task_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'maqola': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'tezis': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'task_type': 'Vazifa turi',
            'maqola': 'Maqola fayli (ixtiyoriy)',
            'tezis': 'Tezis fayli (ixtiyoriy)',
        }


class TaskAssessmentForm(forms.ModelForm):
    class Meta:
        model = TaskSubmission
        fields = ['assessment_comment', 'score']
        widgets = {
            'assessment_comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Izoh kiriting...',
                'rows': 3
            }),
            'score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100
            }),
        }
        labels = {
            'assessment_comment': 'Izoh',
            'score': 'Baholash (0-100)',
        }

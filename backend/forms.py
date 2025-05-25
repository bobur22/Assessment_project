from django import forms
from .models import TaskSubmission, KafedraMaterial, StudentAwards
from user.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class TaskSubmissionForm(forms.ModelForm):
    class Meta:
        model = TaskSubmission
        fields = ['task_upload', 'task_upload_by', 'title', 'date', 'task_type', 'jurnal']
        labels = {
            'task_upload': 'Yuklash turi',
            'task_upload_by': 'Fayl yuklang',
            'title': 'Sarlavha',
            'date': 'Sana',
            'task_type': 'Vazifa turi',
            'jurnal': 'Jurnal nomi',
        }
        widgets = {
            'task_upload': forms.Select(attrs={'class': 'form-select'}),
            'task_upload_by': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'task_type': forms.Select(attrs={'class': 'form-select'}),
            'jurnal': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TaskAssessmentForm(forms.ModelForm):
    class Meta:
        model = TaskSubmission
        fields = ['score', 'assessment_comment']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
            'assessment_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }



class TeacherCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Parolni tasdiqlang')

    class Meta:
        model = User
        fields = ('full_name', 'email', 'p_number', 'teacher_type', 'experience', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Parollar mos kelmadi.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.USTOZ
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class KafedraMaterialForm(forms.ModelForm):
    class Meta:
        model = KafedraMaterial
        fields = ['title', 'kafedraTaskType', 'kafedraUpload', 'date', 'jurnal', 'teachers']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }



class StudentAwardsForm(forms.ModelForm):
    class Meta:
        model = StudentAwards
        fields = [
            'title',
            'task_type',
            'task_upload',
            'file_upload',
            'date',
            'student_fname',
            'student_course',
            'student_kafedra',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'student_fname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student full name'}),
            'student_course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course (e.g., 3rd year)'}),
            'student_kafedra': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kafedra (Department)'}),
        }
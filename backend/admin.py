from django.contrib import admin
from .models import TaskSubmission


@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'teacher',
        'task_type',
        'submitted_at',
        'kafedra',
        'score',
        'assessed_at',
    )
    list_filter = ('task_type', 'submitted_at', 'assessed_at')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'assessment_comment')
    readonly_fields = ('submitted_at', 'assessed_at')

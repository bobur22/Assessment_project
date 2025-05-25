from django.contrib import admin
from .models import TaskSubmission, StudentAwards


@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'teacher',
        'task_type',
        'task_upload',
        'submitted_at',
        'kafedra',
        'score',
        'assessed_at',
    )
    list_filter = (
        'task_type',
        'task_upload',
        'submitted_at',
        'assessed_at',
        'score',
    )
    search_fields = (
        'title',
        'teacher__first_name',
        'teacher__last_name',
        'assessment_comment',
    )
    readonly_fields = ('submitted_at', 'assessed_at')
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'teacher',
                'task_type',
                'task_upload',
                'task_upload_by',
                'date',
                'submitted_at',
            )
        }),
        ('Baholash', {
            'fields': (
                'score',
                'assessment_comment',
                'assessed_at',
                'kafedra',
            )
        }),
    )

admin.site.register(StudentAwards)
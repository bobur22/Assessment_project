from django.conf import settings
from django.db import models
from django.utils import timezone


class TaskSubmission(models.Model):
    class TaskType(models.TextChoices):
        LOCAL = 'local', 'Mahalliy vazifa'
        GLOBAL = 'global', 'Xalqaro vazifa'

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'ustoz'},
        verbose_name="Ustoz",
        related_name='submitted_tasks'
    )
    task_type = models.CharField(
        max_length=10,
        choices=TaskType.choices,
        default=TaskType.LOCAL,
        verbose_name="Vazifa turi"
    )
    maqola = models.FileField(upload_to='maqolalar/', blank=True, null=True)
    tezis = models.FileField(upload_to='tezislar/', blank=True, null=True)
    submitted_at = models.DateTimeField(default=timezone.now)

    kafedra = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'kafedra'},
        verbose_name="Baholagan kafedra",
        related_name='assessed_tasks'
    )
    assessment_comment = models.TextField(blank=True, null=True)
    score = models.PositiveSmallIntegerField(blank=True, null=True)
    assessed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.teacher.get_full_name()} - {self.get_task_type_display()}"

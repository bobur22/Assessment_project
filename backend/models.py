from django.db import models
from django.conf import settings
from datetime import date


class TaskSubmission(models.Model):
    class TaskType(models.TextChoices):
        LOCAL = 'local', 'Mahalliy vazifa'
        GLOBAL = 'global', 'Xalqaro vazifa'

    class TaskUpload(models.TextChoices):
        ARTICLE = 'articles', 'Maqola'
        CERTIFICATE = 'certificates', 'AKT sertifikatlar'
        CREATED = 'created', 'Ixtiro'

    title = models.CharField(max_length=255)

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

    task_upload = models.CharField(
        choices=TaskUpload.choices,
        default=TaskUpload.ARTICLE,
    )

    task_upload_by = models.FileField(upload_to='tasks/', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    jurnal = models.CharField(max_length=255, blank=True, null=True)

    assessment_comment = models.TextField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    assessed_at = models.DateTimeField(blank=True, null=True)

    kafedra = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'kafedra'},
        related_name='assessed_tasks'
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.get_full_name()} - {self.title}"


class KafedraMaterial(models.Model):
    class MaterialType(models.TextChoices):
        BOOKS = 'books', 'Kafedra kitobi'
        INSTRUCTIONS = 'instruction', "O'quv qo'llanma"
        SCIENTIFIC_WORKS = 'scientific_work', 'Ilmiy ish'

    title = models.CharField(max_length=255, default="")
    kafedraTaskType = models.CharField(max_length=100, choices=MaterialType, default=MaterialType.BOOKS)
    kafedraUpload = models.FileField(upload_to='kafedra_files/', blank=True, null=True)
    date = models.DateField(default=date.today)
    jurnal = models.CharField(max_length=255, default="")
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='materials', default="",
                                      limit_choices_to={'role': 'ustoz'}, )
    kafedra = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_materials',
                                default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class StudentAwards(models.Model):
    class StudentType(models.TextChoices):
        LOCAL = 'local', 'Mahalliy vazifa'
        GLOBAL = 'global', 'Xalqaro vazifa'

    class AwardsType(models.TextChoices):
        OLIMPICS = 'olimpics', 'Olimpiada'
        COMPETITION = 'competition', 'Musoboqa'
        STUDENT_EMP = 'student_employment', 'Talaba bandligi'

    title = models.CharField(max_length=255)

    task_type = models.CharField(
        choices=StudentType.choices,
        default=StudentType.LOCAL,
        verbose_name="Vazifa turi"
    )

    task_upload = models.CharField(
        choices=AwardsType.choices,
        default=AwardsType.OLIMPICS,
        verbose_name="Mukofot turi"
    )

    file_upload = models.FileField(upload_to='student_award/', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    student_fname = models.CharField(max_length=255, blank=True, null=True)
    student_course = models.CharField(max_length=100, blank=True, null=True)
    student_kafedra = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


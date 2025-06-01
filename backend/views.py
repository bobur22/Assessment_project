from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count

from .models import TaskSubmission, KafedraMaterial, StudentAwards
from user.models import User
from .forms import TaskSubmissionForm, TaskAssessmentForm, TeacherCreateForm, KafedraMaterialForm, StudentAwardsForm

from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


# Utility functions to check roles
def is_teacher(user):
    return user.is_authenticated and user.role == 'ustoz'


def is_kafedra(user):
    return user.is_authenticated and user.role == 'kafedra'


def is_dekan(user):
    return user.is_authenticated and user.role == 'dekan'


def is_award_user(user):
    return user.is_authenticated and user.role == 'award_manager'


def is_award_user_or_dekan(user):
    return user.is_authenticated and (
            user.role == User.Role.KAFEDRA or user.role == User.Role.DEKAN or user.role == User.Role.AWARD_MANAGER or user.role == User.Role.USTOZ)


def is_kafedra_or_dekan(user):
    return user.is_authenticated and (user.role == User.Role.KAFEDRA or user.role == User.Role.DEKAN)


# ======================= Teacher Views =======================


def home_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == 'ustoz':
            return redirect('teacher-task-list')
        elif request.user.role == 'kafedra':
            return redirect('kafedra-task-list')
        elif request.user.role == 'dekan':
            return redirect('dekan-dashboard')
        elif request.user.role == 'award_manager':
            return redirect('awards_list')
    # ✅ Always return something
    return redirect('login')  # or a default homepage


@login_required
@user_passes_test(is_teacher)
def teacher_task_list(request):
    tasks = TaskSubmission.objects.filter(teacher=request.user).order_by('-submitted_at')
    t_count = tasks.count()
    return render(request, 'tasks/teacher_task_listV2.html', {'tasks': tasks, 't_count': t_count})


@login_required
@user_passes_test(is_teacher)
def upload_task(request):
    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.teacher = request.user
            task.save()
            messages.success(request, 'Vazifa muvaffaqiyatli yuklandi!')
            return redirect('teacher-task-list')  # adjust as needed
        else:
            messages.error(request, "Iltimos, formani to'g'ri to'ldiring.")
    else:
        form = TaskSubmissionForm()

    return render(request, 'tasks/upload_taskV2.html', {'form': form})


# ======================= Kafedra Views =======================

@login_required
@user_passes_test(is_kafedra)
def kafedra_task_list(request):
    tasks = TaskSubmission.objects.filter(score__isnull=True).order_by('-submitted_at')
    t_count = tasks.count()
    return render(request, 'tasks/kafedra_task_listV2.html', {'tasks': tasks, 't_count': t_count})


@login_required
def kafedra_assessed_tasks(request):
    if request.user.role != 'kafedra':
        return redirect('login')  # Optional: restrict access

    tasks = TaskSubmission.objects.filter(
        kafedra=request.user,
        score__isnull=False  # Only those with a score
    ).order_by('-assessed_at')
    t_tasks = tasks.count()

    return render(request, 'tasks/kafedra_assessed_tasksV2.html', {'tasks': tasks, 't_tasks': t_tasks})


@login_required
@user_passes_test(is_kafedra)
def assess_task(request, task_id):
    task = get_object_or_404(TaskSubmission, id=task_id)
    if request.method == 'POST':
        form = TaskAssessmentForm(request.POST, instance=task)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.kafedra = request.user
            assessment.assessed_at = now()
            assessment.save()
            messages.success(request, 'Vazifa baholandi!')
            return redirect('kafedra-task-list')
    else:
        form = TaskAssessmentForm(instance=task)
    return render(request, 'tasks/assess_taskV2.html', {'task': task, 'form': form})


# ======================= Dekan Views =======================


@login_required
@user_passes_test(is_kafedra_or_dekan)
def dekan_dashboard(request):
    kafedra = User.objects.all().filter(role=User.Role.KAFEDRA).count()
    ustoz = User.objects.all().filter(role=User.Role.USTOZ).count()
    award = StudentAwards.objects.all().count()
    tasks = TaskSubmission.objects.all().count()
    tasks = round(tasks / ustoz / 2 * tasks)

    print(kafedra, ustoz, award, tasks)
    return render(request, 'dashboard/dashboardV2.html', {'kafedra': kafedra, 'ustoz': ustoz, 'tasks': tasks, 'award': award})


@login_required
@user_passes_test(is_kafedra_or_dekan)
def dashboard_data(request):
    # Example: Count of TaskSubmissions by task_type
    task_type_counts = TaskSubmission.objects.values('task_type').annotate(count=Count('id'))
    task_type_data = {item['task_type']: item['count'] for item in task_type_counts}

    # Example: Count of StudentAwards by task_type
    award_type_counts = StudentAwards.objects.values('task_type').annotate(count=Count('id'))
    award_type_data = {item['task_type']: item['count'] for item in award_type_counts}

    return JsonResponse({
        'task_type_data': task_type_data,
        'award_type_data': award_type_data,
    })


@login_required
@user_passes_test(is_dekan)
def dekan_task_list(request):
    tasks = TaskSubmission.objects.all().order_by('-submitted_at')
    t_count = tasks.count()
    return render(request, 'tasks/assess_task_listV2.html', {'tasks': tasks, 't_count': t_count})


# ======================= Kafedra Teacher Views =======================


@login_required
@user_passes_test(is_kafedra_or_dekan)
def teacher_list_view(request):
    teachers = User.objects.filter(role=User.Role.USTOZ)
    t_count = teachers.count()
    return render(request, 'kafedra/teacher_listV2.html', {'teachers': teachers, 't_count': t_count})


@login_required
@user_passes_test(is_kafedra)
def teacher_create_view(request):
    if request.method == 'POST':
        form = TeacherCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherCreateForm()
    return render(request, 'kafedra/teacher_createV2.html', {'form': form})


# ======================= Awards manager Views =======================


@login_required
@user_passes_test(is_award_user)
def create_student_award(request):
    if request.method == 'POST':
        form = StudentAwardsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('awards_list')
        else:
            print(form.errors)
    else:
        form = StudentAwardsForm()
    return render(request, 'awards/create_awardV2.html', {'form': form})


@login_required
@user_passes_test(is_award_user_or_dekan)
def awards_list(request):
    awards = StudentAwards.objects.all().order_by('-created_at')
    return render(request, 'awards/awards_listV2.html', {'awards': awards})


# ======================= Kafedra Materialls Views =======================


class MaterialListView(LoginRequiredMixin, ListView):
    model = KafedraMaterial
    template_name = 'kafedra/material_listV2.html'
    context_object_name = 'materials'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material_count'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        user = self.request.user
        if user.role == 'kafedra':
            return KafedraMaterial.objects.filter(kafedra=user)
        elif user.role == 'ustoz':
            return KafedraMaterial.objects.filter(teachers=user)
        elif user.role == 'dekan':
            return KafedraMaterial.objects.all()
        return KafedraMaterial.objects.none()


class MaterialCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = KafedraMaterial
    form_class = KafedraMaterialForm
    template_name = 'kafedra/material_createV2.html'
    success_url = reverse_lazy('material_list')

    def form_valid(self, form):
        form.instance.kafedra = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.role == 'kafedra'

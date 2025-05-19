from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from django.contrib import messages

from .models import TaskSubmission
from .forms import TaskSubmissionForm, TaskAssessmentForm


# Utility functions to check roles
def is_teacher(user):
    return user.is_authenticated and user.role == 'ustoz'

def is_kafedra(user):
    return user.is_authenticated and user.role == 'kafedra'

def is_dekan(user):
    return user.is_authenticated and user.role == 'dekan'


# ======================= Teacher Views =======================


def home_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == 'ustoz':
            return redirect('teacher-task-list')
        elif request.user.role == 'kafedra':
            return redirect('kafedra-task-list')
        elif request.user.role == 'dekan':
            return redirect('dekan-task-list')
    else:
        return redirect('login')


@login_required
@user_passes_test(is_teacher)
def teacher_task_list(request):
    tasks = TaskSubmission.objects.filter(teacher=request.user).order_by('-submitted_at')
    return render(request, 'tasks/teacher_task_list.html', {'tasks': tasks})


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
            return redirect('teacher-task-list')
    else:
        form = TaskSubmissionForm()
    return render(request, 'tasks/upload_task.html', {'form': form})


# ======================= Kafedra Views =======================

@login_required
@user_passes_test(is_kafedra)
def kafedra_task_list(request):
    tasks = TaskSubmission.objects.filter(score__isnull=True).order_by('-submitted_at')
    return render(request, 'tasks/kafedra_task_list.html', {'tasks': tasks})


@login_required
def kafedra_assessed_tasks(request):
    if request.user.role != 'kafedra':
        return redirect('login')  # Optional: restrict access

    tasks = TaskSubmission.objects.filter(
        kafedra=request.user,
        score__isnull=False  # Only those with a score
    ).order_by('-assessed_at')

    return render(request, 'tasks/kafedra_assessed_tasks.html', {'tasks': tasks})


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
    return render(request, 'tasks/assess_task.html', {'task': task, 'form': form})


# ======================= Dekan Views =======================

@login_required
@user_passes_test(is_dekan)
def dekan_task_list(request):
    tasks = TaskSubmission.objects.all().order_by('-submitted_at')
    return render(request, 'tasks/dekan_task_list.html', {'tasks': tasks})

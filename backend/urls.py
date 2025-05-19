from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home-redirect'),

    # Teacher URLs
    path('teacher/tasks/', views.teacher_task_list, name='teacher-task-list'),
    path('teacher/upload/', views.upload_task, name='upload-task'),

    # Kafedra URLs
    path('kafedra/tasks/', views.kafedra_task_list, name='kafedra-task-list'),
    path('kafedra/assessed/', views.kafedra_assessed_tasks, name='kafedra-assessed-tasks'),
    path('kafedra/assess/<int:task_id>/', views.assess_task, name='assess-task'),

    # Dekan URLs
    path('dekan/tasks/', views.dekan_task_list, name='dekan-task-list'),
]

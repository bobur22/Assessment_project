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

    # Kafedra teacher URLs
    path('teachers/', views.teacher_list_view, name='teacher_list'),
    path('teachers/create/', views.teacher_create_view, name='teacher_create'),

    # Kafedra teacher URLs
    path('materials/', views.MaterialListView.as_view(), name='material_list'),
    path('materials/create/', views.MaterialCreateView.as_view(), name='material_create'),

    # Dekan URLs
    path('dekan/tasks/', views.dekan_task_list, name='dekan-task-list'),
    path('dekan/dashboard/', views.dekan_dashboard, name='dekan-dashboard'),
    path('dekan/dashboard/data/', views.dashboard_data, name='dashboard-data'),

    # Awards manager URLs
    path('awardsManager/create/', views.create_student_award, name='create_student_award'),
    path('awardsManager/list/', views.awards_list, name='awards_list'),
]

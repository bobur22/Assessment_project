from django.urls import path
from .views import logout_view, login_view

urlpatterns = [
    path('log-in/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
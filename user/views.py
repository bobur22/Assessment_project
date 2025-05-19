from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

User = get_user_model()

def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('login')
            else:
                form.add_error('password', 'Username yoki parol noto\'g\'ri')
    return render(request, "accounts/sign-in.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
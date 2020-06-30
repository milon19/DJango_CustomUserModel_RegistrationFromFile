from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.contrib.auth.views import (LogoutView, LoginView, PasswordChangeView,
                                       PasswordChangeDoneView)
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def HomeView(request):
    return render(request, 'home.html')


class LogoutView(LogoutView):
    next_page = 'home'


class LoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'users/login.html'


@login_required
def ProfileView(request):
    return render(request, 'users/profile.html')


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'


class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'users/password_change_form.html'


class PasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'



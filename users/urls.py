from django.urls import path
from .views import (HomeView, LogoutView, LoginView, ProfileView,
                    RegisterView, PasswordChangeView, PasswordChangeDoneView)

urlpatterns = [
    path('', HomeView, name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView, name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]

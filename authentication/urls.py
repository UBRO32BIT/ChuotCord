from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from . import views
urlpatterns = [
    path('login/', views.SignInView.as_view(), name="login"),
    path('register/', views.SignUpView.as_view(), name="register"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('password-reset/', PasswordResetView.as_view(template_name='authentication/password-reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='authentication/password-reset-done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='authentication/password-reset-confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='authentication/password-reset-complete.html'),name='password_reset_complete'),
]
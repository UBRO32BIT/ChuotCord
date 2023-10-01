from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.SignInView.as_view(), name="login"),
    path('register/', views.SignUpView.as_view(), name="register"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
]
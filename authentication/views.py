from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from home.views import index
from .forms import LoginForm

# Create your views here.
def check_if_not_authenticated(user):
    return not user.is_authenticated

@csrf_protect
@user_passes_test(check_if_not_authenticated)
def loginView(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            messages.success(request, ("There was an error while logging, please try again!"))
            return redirect('login')
    else:
        form_login = LoginForm()
        return render(request, 'authentication/login.html', {'form_login': form_login})
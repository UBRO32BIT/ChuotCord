from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from home.views import index
from .forms import LoginForm, RegisterForm
from chat.models import GroupUser, Group
# Create your views here.
def check_if_not_authenticated(user):
    return not user.is_authenticated

@csrf_protect
@user_passes_test(check_if_not_authenticated)
def sign_in(request):
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
        return render(request, 'authentication/login.html', {'form': form_login})

@user_passes_test(check_if_not_authenticated)
def sign_up(request):
    if (request.method == 'GET'):
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'authentication/register.html', context)
    
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')

            group = Group.objects.get(id=1)
            group_add = GroupUser(group=group, member=user)
            group_add.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'authentication/register.html', {'form': form})
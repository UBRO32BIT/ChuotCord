import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views import View
from home.views import index
from .forms import LoginForm, RegisterForm
from chat.models import GroupUser, Group
from chuotcord.settings import RECAPTCHA_SECRET_KEY, RECAPTCHA_SITE_KEY

def check_if_not_authenticated(user):
    return not user.is_authenticated
def verify_recaptcha(token):
    data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': token,
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = response.json()
    return result.get('success')

class SignInView(View):
    @method_decorator(csrf_protect)
    @method_decorator(user_passes_test(check_if_not_authenticated))
    def get(self, request):
        form_login = LoginForm()
        return render(request, 'authentication/login.html', {'form': form_login})

    @method_decorator(csrf_protect)
    @method_decorator(user_passes_test(check_if_not_authenticated))
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            messages.error(request, "There was an error while logging in, please try again!")
            return redirect('login')

class SignUpView(View):
    @method_decorator(user_passes_test(check_if_not_authenticated))
    def get(self, request):
        form = RegisterForm()
        context = {'form': form, 'site_key': RECAPTCHA_SITE_KEY}
        return render(request, 'authentication/register.html', context)

    @method_decorator(user_passes_test(check_if_not_authenticated))
    def post(self, request):
        captcha_result = verify_recaptcha(request.POST.get('g-recaptcha-response'))
        form = RegisterForm(request.POST)
        if captcha_result and form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have signed up successfully.')

            group = Group.objects.get(id=1)
            group_add = GroupUser(group=group, member=user)
            group_add.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'There were an error while registering, please try again!')
            return render(request, 'authentication/register.html', {'form': form, 'site_key': RECAPTCHA_SITE_KEY})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logout successful!')
        return redirect('home')
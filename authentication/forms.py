from django import forms
class LoginForm(forms.Form):
    username = forms.CharField(label='User name', max_length=20)
    password = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput)
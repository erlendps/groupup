from django import forms

class LoginForm(forms.form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.PasswordInput(label="Password")

class RegisterForm(forms.form):
    username = forms.CharField(label="Username", max_length=100)

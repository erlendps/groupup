from unittest.util import _MAX_LENGTH
from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    profile_pic = forms.ImageField(label="profile_pic")
    interests = forms.BooleanField(label="interests")
    dateofbirth = forms.DateField(label="dateofbirth")

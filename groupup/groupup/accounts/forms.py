from dataclasses import fields
from django import forms
from .models import Interest
from .widgets import DatePickerInput


class RegisterForm(forms.Form):
    """Form for creating a new groupupuser"""
    
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    profile_pic = forms.ImageField(label="profile_pic")
    interests = forms.ModelMultipleChoiceField(
                                    label="interests",
                                    queryset=Interest.objects.all(),
                                    widget=forms.CheckboxSelectMultiple)
    birthday = forms.DateField(label="dateofbirth", widget=DatePickerInput)

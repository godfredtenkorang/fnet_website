from django.contrib.auth.forms import AuthenticationForm
from django import forms

from django.forms.widgets import PasswordInput, TextInput


# Login form

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'required': 'required'
    }), label='')
    password = forms.CharField(widget=PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'required': 'required'
    }), label='')
    

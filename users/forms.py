from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    
    role = forms.ChoiceField(
        choices=[("customer", "Customer"), ("driver", "Driver"), ("agent", "Agent")],  # Removed "Admin"
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'phone', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'required': 'required'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'required': 'required'}),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'required': 'required'}),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password',
                'required': 'required'}),
            'role': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        
        
        
        
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
    
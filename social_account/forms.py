from django import forms
from django.contrib.auth.models import User

from .models import Profile

class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['date_of_birth', "photo"]

    def clean_email(self):
        data=self.cleaned_data['email']
        qs=User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email is already used')
        return data

class LoginForm(forms.Form):
    username=forms.CharField(empty_value='Enter your username or email', label='Enter your username or email')
    password=forms.CharField(widget=forms.PasswordInput(), empty_value='Enter password',)


class UserRegistrationForm(forms.ModelForm):
    password =forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 =forms.CharField(label='Retype password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        else:
            return cd['password2']
        
    def clean_email(self):
        data=self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email is already used')
        return data
    

from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username=forms.CharField(empty_value='Enter your username or email')
    password=forms.CharField(widget=forms.PasswordInput(), empty_value='Enter password')


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

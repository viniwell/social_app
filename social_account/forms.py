from django import forms

class LoginForm(forms.Form):
    username=forms.CharField(empty_value='Enter your username or email')
    password=forms.CharField(widget=forms.PasswordInput(), empty_value='Enter pasword')

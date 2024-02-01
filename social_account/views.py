from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'social_account/dashboard.html', {'section':'dashboard'})

@login_required
def edit(request):
    if request.POST:
        user_form=UserEditForm(instance=request.user, data=request.POST)
        profile_form =ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
    return render(request, 'social_account/edit.html', {'user_form':user_form,  
                                                      'profile_form':profile_form},
                                                      )

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form=LoginForm()
    return render(request, 'social_account/login.html', {'form':form})

def register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'social_account/register_done.html', {'new_user':new_user})

    else:
        form=UserRegistrationForm()
    return render(request,'social_account/register.html',{'form':form})
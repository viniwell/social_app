from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


# Create your views here.

@login_required
def dashboard(request:HttpRequest):
    try:
        print(request.ms)
        for m in request.ms:
            messages.success(request=request, message=m)
    except Exception as e:
        print(e)

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

def user_logout(request:HttpRequest):
    logout(request)
    return dashboard(request)

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

@login_required
def edit(request:HttpRequest):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            ms=["Profile updated"]
            #return redirect(to=dashboard, kwargs={'meseges':["Profile updated!"]})
            r=HttpRequest()
            for key, value in request.__dict__.items():
                r.__setattr__(key,value)
            r.__setattr__('method', 'GET')
            r.__setattr__('ms', ms)
            r.__setattr__('user', request.user)
            return dashboard(r)
        else:
            messages.error(request, 'Some error occured')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'social_account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
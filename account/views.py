from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', context={'form': form})

@login_required
def page_profile(request):
    return render(request, 'account/profile.html', context={'section': 'profile'})

def register(request):
    if request.method =='POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #Создаем нового пользователя но в БД не сохраняем
            new_user = user_form.save(commit=False)
            #Задаем пользователю зашифрованный пароль
            new_user.set_password(user_form.cleaned_data['password'])
            #сохраняем в БД
            new_user.save()
            Profile.objects.create(user=new_user)

            return render(request, 'account/register_done.html', context={'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', context={'user_form': user_form})

@login_required
def edit(request):
    if request.method =='POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data= request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', context={'user_form':user_form, 'profile_form':profile_form})

def userid_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'account/userid_profile.html', context={'user': user})
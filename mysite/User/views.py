# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from .forms import UserForm


# Create your views here.


def register(request):
    if request.method != 'POST':
        login_form = AuthenticationForm()
        register_form = UserCreationForm()
    else:
        register_form = UserCreationForm(data=request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.save()
            return HttpResponseRedirect(reverse('index'))
    context = {'form': login_form, 'register_form': register_form}
    return render(request, 'User/register.html', context)


@login_required
def profile(request):
    return render(request, 'User/profile.html')


@login_required
def change_profile(request):
    if request.method != "POST":
        change_profile_form = UserForm(instance=request.user)
    else:
        change_profile_form = UserForm(data=request.POST, instance=request.user)
        if change_profile_form.is_valid():
            user = change_profile_form.save(commit=False)
            user.save()
            return HttpResponseRedirect(reverse('User:profile'))
    context = {'change_profile_form': change_profile_form}
    return render(request, 'User/change_profile.html', context)

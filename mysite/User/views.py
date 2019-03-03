# -*- coding: utf-8 -*-
from django.shortcuts import render, reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
# Create your views here.

def index(request):
    return render(request, 'User/index.html')

def register(request):
    """注册用户"""
    if request.method != 'POST':
        # 显示空的注册表单
        form = UserCreationForm()
    else:
        # 提交填好的注册表
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            # new_user = form.save()
            # # 注册后的用户 直接登录， 重定向到首页
            # authenticated_user = authenticate(username=new_user.username, password=request.POST.get('password1', ""))
            # login(request, authenticated_user)
            return HttpResponseRedirect(reverse('User:login'))
    context = {'form': form}
    return render(request, 'User/register.html', context)

@login_required
def profile(request):
    return render(request, 'User/profile.html')

@login_required
def change_email(request):
    return render(request, 'User/change_email.html')
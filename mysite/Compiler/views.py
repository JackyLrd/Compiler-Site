import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from .forms import TaskForm
from .models import Task


# Create your views here.

@login_required
def index(request):
    # ret = subprocess.getstatusoutput("cd cpp_compile; make")
    try:
        task_list = Task.objects.filter(user=request.user)
    except Task.DoesNotExist:
        task_list = []
    context = {'task_list': task_list}
    return render(request, 'Compiler/index.html', context)


@login_required
def create_task(request):
    # if request.method != 'POST':
    #     create_task_form = UploadFileForm()
    # ret = subprocess.getstatusoutput("dir")
    # context = {'ret': ret[1]}
    # return render(request, 'Compiler/create_task.html', context)

    if request.method == 'POST':
        create_task_form = TaskForm(request.POST, request.FILES)
        if create_task_form.is_valid():
            new_task = Task(task_name=create_task_form.cleaned_data['task_name'], user=request.user)
            new_task.save()
            print(os.getcwd(), request.user.id)
            header_dir_name = os.getcwd() + '\\uploaded_files\\' + str(request.user.id) + '\\' + str(
                new_task.id) + '\\include'
            src_dir_name = os.getcwd() + '\\uploaded_files\\' + str(request.user.id) + '\\' + str(new_task.id) + '\\src'
            handle_uploaded_file(request.FILES.getlist('header_file'), header_dir_name)
            handle_uploaded_file(request.FILES.getlist('source_file'), src_dir_name)
            return HttpResponseRedirect(reverse('Compiler:create_success'))
    else:
        create_task_form = TaskForm()
    context = {'create_task_form': create_task_form}
    return render(request, 'Compiler/create_task.html', context)


def handle_uploaded_file(uploaded_file_list, dir_name):
    if os.path.exists(dir_name):
        pass
    else:
        os.makedirs(dir_name)
    for uploaded_file in uploaded_file_list:
        with open(dir_name + '\\' + uploaded_file.name, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

# @login_required
# def modify_task(request):
#     if request.method == 'POST':
#         modify_task_form = TaskForm(request.POST, request.FILES)
#         if modify_task_form.is_valid():
#             new_task = Task(task_name=create_task_form.cleaned_data['task_name'], user=request.user)
#             new_task.save()
#             print(os.getcwd(), request.user.id)
#             dir_name = os.getcwd() + '\\uploaded_files\\' + str(request.user.id) + '\\' + str(new_task.id)
#             if os.path.exists(dir_name):
#                 message = 'OK, the "%s" dir exists.'
#                 print(message % dir_name)
#             else:
#                 message = 'Sorry, I cannot find the "%s" dir.'
#                 print(message % dir_name)
#                 os.makedirs(dir_name)
#             handle_uploaded_file(request.FILES['file'], dir_name)
#
#             return HttpResponseRedirect(reverse('Compiler:create_success'))
#     else:
#         modify_task_form = TaskForm(task_name=)
#     context = {'modify_task_form': modify_task_form}
#     return render(request, 'Compiler/modify_task.html', context)

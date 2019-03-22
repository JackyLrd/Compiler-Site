import os
import subprocess

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render, reverse

from .forms import TaskForm
from .models import Task
from django.contrib import messages



# Create your views here.

@login_required
def index(request):
    try:
        task_list = Task.objects.filter(user=request.user)
    except Task.DoesNotExist:
        task_list = []
    context = {'task_list': task_list}
    return render(request, 'Compiler/index.html', context)


@login_required
def create_task(request):
    if request.method == 'POST':
        create_task_form = TaskForm(request.POST, request.FILES)
        if create_task_form.is_valid():
            new_task = Task(task_name=create_task_form.cleaned_data['task_name'], user=request.user)
            new_task.save()
            header_dir_name = get_dir(request.user.id, new_task.id) + 'include'
            src_dir_name = get_dir(request.user.id, new_task.id) + 'src'
            handle_uploaded_file(request.FILES.getlist('header_file'), header_dir_name)
            handle_uploaded_file(request.FILES.getlist('source_file'), src_dir_name)
            dir_check(get_dir(request.user.id, new_task.id) + 'obj')
            dir_check(get_dir(request.user.id, new_task.id) + 'bin')
            return HttpResponseRedirect(reverse('Compiler:create_success'))
    else:
        create_task_form = TaskForm()
    context = {'create_task_form': create_task_form}
    return render(request, 'Compiler/create_task.html', context)


@login_required
def check_task(request):
    if request.method == 'POST':
        modify_task_form = TaskForm(request.POST, request.FILES)
        if modify_task_form.is_valid():
            task_id = request.POST['task_id']
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                task = None
            if task != None:
                task.task_name = modify_task_form.cleaned_data['task_name']
                task.compile_option = modify_task_form.cleaned_data['compile_option']
                task.save()
                header_dir_name = get_dir(request.user.id, task.id) + 'include'
                src_dir_name = get_dir(request.user.id, task.id) + 'src'
                handle_uploaded_file(request.FILES.getlist('header_file'), header_dir_name)
                handle_uploaded_file(request.FILES.getlist('source_file'), src_dir_name)
            return HttpResponseRedirect(reverse('Compiler:modify_success'))
        context = {'modify_task_form': modify_task_form}
    else:
        task_id = request.GET.get('task_id')
        header_file_list = []
        src_file_list = []
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            task = None
        if task != None:
            task_state = check_process(request.user.id, task.id)
            modify_task_form = TaskForm({'task_name': task.task_name, 'compile_option': task.compile_option})
            header_dir_name = get_dir(request.user.id, task.id) + 'include'
            header_file_list = get_dir_file_list(header_dir_name)
            src_dir_name = get_dir(request.user.id, task.id) + 'src'
            src_file_list = get_dir_file_list(src_dir_name)
            try:
                with open(get_dir(request.user.id, task.id) + 'compile_daemon.log', 'r') as f:
                    compile_output = f.readlines()
                    for line in compile_output:
                        line = line.rstrip('\n')
            except FileNotFoundError:
                compile_output = []
        context = {'modify_task_form': modify_task_form,
                   'header_file_list': header_file_list,
                   'src_file_list': src_file_list,
                   'task_id': task_id,
                   'task_name': task.task_name,
                   'task_state': task_state,
                   'compile_output': compile_output}
    return render(request, 'Compiler/check_task.html', context)


@login_required
def start_compile(request):
    if request.method == 'POST':
        task_id = request.POST['task_id']
        context = {'task_id': task_id}
    else:
        task_id = request.GET['task_id']
        is_running = check_process(request.user.id, task_id)
        if is_running:
            pass
        else:
            pid_file = get_dir(request.user.id, task_id) + 'compile_daemon.pid'
            log_file = get_dir(request.user.id, task_id) + 'compile_daemon.log'
            dir_name = get_dir(request.user.id, task_id)
            task = Task.objects.get(id=task_id)
            compile_option = task.compile_option.replace('-', '_')
            cmd = ['sh', 'compile_daemon.sh', pid_file, log_file, dir_name, compile_option]
            compile_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='./uploaded_files/')
            compile_proc.wait()
            compile_proc.kill()
        task_id = request.GET.get('task_id')
        context = {'task_id': task_id, 'is_running': is_running}
    return render(request, 'Compiler/start_compile.html', context)


@login_required
def stop_compile(request):
    if request.method == 'POST':
        task_id = request.POST['task_id']
        context = {'task_id': task_id}
    else:
        task_id = request.GET['task_id']
        is_running = check_process(request.user.id, task_id)
        if is_running:
            kill_cmd = 'kill `cat ./compile_daemon.pid`'
            kill_proc = subprocess.Popen(kill_cmd, shell=True, cwd=get_dir(request.user.id, task_id))
            kill_proc.wait()
            kill_proc.kill()
        else:
            pass
        context = {'task_id': task_id, 'is_running': is_running}
    return render(request, 'Compiler/stop_compile.html', context)


@login_required
def get_target(request):
    if request.method == 'POST':
        pass
    else:
        task_id = request.GET['task_id']
        bin_dir_name = get_dir(request.user.id, task_id) + 'bin'
        try:
            return FileResponse(open(bin_dir_name + '/target', 'rb'), filename="target", as_attachment=True)
        except FileNotFoundError:
            return

def handle_uploaded_file(uploaded_file_list, dir_name):
    dir_check(dir_name)
    for uploaded_file in uploaded_file_list:
        with open(dir_name + '/' + uploaded_file.name, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)


def dir_check(dir_name):
    if os.path.exists(dir_name):
        pass
    else:
        os.makedirs(dir_name)


def get_dir_file_list(dir_name):
    if os.path.exists(dir_name):
        return os.listdir(dir_name)
    else:
        return []


def get_dir(user_id, task_id):
    return os.getcwd() + '/uploaded_files/' + str(user_id) + '/' + str(task_id) + '/'


def check_process(user_id, task_id):
    check_cmd = 'ps -elf | grep `cat ./compile_daemon.pid`'
    check_proc = subprocess.Popen(check_cmd, shell=True, cwd=get_dir(user_id, task_id), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check_proc.wait()
    check_proc.kill()
    if check_proc.returncode == 0:
        return True
    return False

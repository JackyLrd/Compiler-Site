from django.shortcuts import render

from django.http import HttpResponse
import subprocess


# Create your views here.

def index(request):
    ret = subprocess.getstatusoutput("cd cpp_compile; make")
    print(ret)
    return HttpResponse(ret[1])
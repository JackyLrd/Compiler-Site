import subprocess

from django.http import HttpResponse


# Create your views here.


def index(request):
    ret = subprocess.getstatusoutput("cd cpp_compile; make")
    print(ret)
    return HttpResponse(ret[1])

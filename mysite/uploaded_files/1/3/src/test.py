import subprocess

ret = subprocess.getstatusoutput("make")
print(ret)

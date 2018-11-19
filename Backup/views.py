from django.shortcuts import render
from subprocess import check_output
import subprocess
from django.contrib import messages
# Create your views here.
def V_BackupIndex(request):
    return render(request,'Backup/index.html')

def V_DoBackup(request):
    try:
        check_output("cd C:\\Program Files (x86)\\PostgreSQL\\9.6\\bin", shell=True,stderr=subprocess.STDOUT).decode()
        check_output("pg_dump -h 192.168.7.83 -U pi postgres > C:\\postgres.bak", shell=True,stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        messages.error(request, "備份失敗!command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output), extra_tags='alert')


    messages.success(request, '備份成功!', extra_tags='alert')
    return render(request,'Backup/index.html')

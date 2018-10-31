from django.shortcuts import render
from django.http import HttpResponse
from EmployeeCard.models import M_EmployeeCard
from django.core import serializers
import datetime
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def V_EmployeeCardIndex(request):
    return render(request,'EmployeeCard/index.html')


def V_GetEmployeeCardData(request):
    try:
        EmployeeCardData=M_EmployeeCard.objects.all()
    except:
        EmployeeCardData=''
    EmployeeCardDataJson = serializers.serialize('json', EmployeeCardData)
    return HttpResponse(EmployeeCardDataJson, content_type='application/json')


def V_EmployeeCardEdit(request,id):
    if(id==0):
        EmployeeCardData=None
    else:
        EmployeeCardData=M_EmployeeCard.objects.get(pk=id).__dict__
    return render(request,'EmployeeCard/Edit.html',EmployeeCardData);


def V_EmployeeCardSave(request):
    EmployeeID = request.POST.get('EmployeeID', '')
    EmployeeName = request.POST.get('EmployeeName', '')
    CardNo = request.POST.get('CardNo', '')
    IsWork = request.POST.get('IsWork', 'False')
    pk = request.POST.get('pk', '')

    if(pk!=''):
        EmployeeCardData=M_EmployeeCard.objects.get(pk=pk)
    else:
        EmployeeCardData=M_EmployeeCard()
        user = User.objects.create_user(EmployeeID, 'XXX@XXX.XXX', '123456789')
        user.save()
    EmployeeCardData.EmployeeID=EmployeeID
    EmployeeCardData.EmployeeName=EmployeeName
    EmployeeCardData.CardNo=CardNo
    EmployeeCardData.IsWork=IsWork
    EmployeeCardData.Editor=request.user
    EmployeeCardData.EditDate=datetime.datetime.now()
    EmployeeCardData.save()

    messages.success(request, '儲存成功!', extra_tags='alert')
    return render(request,'EmployeeCard/index.html')

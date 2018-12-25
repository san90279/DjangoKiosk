from django.shortcuts import render,redirect
from django.http import HttpResponse
from PrintData.models import M_PrintData
import datetime,json
from django.views.decorators.csrf import csrf_protect
from CommonApp.models import GridCS
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from PrintData.forms import PrintDataForm
from django.core import serializers
from datetime import timedelta
# Create your views here.

def V_PrintDataIndex(request):
    return render(request,'PrintData/index.html');

@csrf_protect
def V_GetPrintData(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數
    #將前端request物件傳入GridCS內做處理
    grid=GridCS(request)
    #將Model M_Penalty傳入作查詢
    PrintData=grid.dynamic_query_order(M_PrintData)
    #將PenaltyData傳入作後端分頁
    object_list = grid.dynamic_query_order_paginator(PrintData)
    #資料總筆數
    count=len(PrintData)
    #拼出teplate JQGRID 欄位JSON資料流
    data=[{	'EnableDate': (Print.EnableDate+timedelta(hours=8)).strftime("%Y-%m-%d"),
			'Salesman': Print.Salesman,
            'Accounting': Print.Accounting,
            'Chief': Print.Chief,
            'Tel': Print.Tel,
			'Fax': Print.Fax,
            'pk': Print.pk} for Print in object_list]
    #JQGRID API
    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }
    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')


def V_EditPrintData(request, id):
    PrintData = M_PrintData.objects.get(id=id)
    template = 'PrintData/Edit.html'
    if request.method == 'GET':
        form = PrintDataForm(instance=PrintData)
        return render(request, template, {'form':form})

    # POST
    form = PrintDataForm(request.POST, instance=PrintData)
    if not form.is_valid():
        return render(request, template, {'form':form})
    else:
        PrintData = form.save(commit=False)
        PrintData.Editor = request.user
        PrintData.EditDate = datetime.datetime.now()
        PrintData.save()
        messages.success(request, '發票資訊編輯成功!', extra_tags='alert')
        return redirect('PrintDataIndex')


def V_NewPrintData(request):
    template = 'PrintData/Edit.html'
    if request.method == "POST":
        form = PrintDataForm(request.POST)
        if form.is_valid():
            PrintData = form.save(commit=False)
            PrintData.EnableDate = form.EnableDate+timedelta(hours=8)
            PrintData.Salesman = form.Salesman
            PrintData.Accounting = form.Accounting
            PrintData.Chief = form.Chief
            PrintData.Tel = form.Tel
            PrintData.Fax = form.Fax
            PrintData.Editor = request.user
            PrintData.EditDate = datetime.datetime.now()
            PrintData.save()
            messages.success(request, '發票資訊新增成功!', extra_tags='alert')
            return redirect('PrintDataIndex')
    else:
        form = PrintDataForm()
    return render(request, template, {'form': form})

def V_GetLastPrintData(request):
    data=M_PrintData.objects.filter(EnableDate__lte=datetime.datetime.now()).order_by('-EnableDate','-id')
    if(len(data)>0):
        dump = serializers.serialize('json', data.only())
        return HttpResponse(dump, content_type='application/json')
    return HttpResponse('', content_type='application/json')

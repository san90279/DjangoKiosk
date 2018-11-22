from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from Invoice.models import M_Invoice,M_V_Invoice
from FeeItem.models import M_FeeItem
from Store.models import M_Station
import datetime,json
from CommonApp.models import GridCS
from django.core.serializers.json import DjangoJSONEncoder
from Invoice.forms import AddInvoiceForm
from django.db.models import Max
from django.contrib import messages

# Create your views here.
def V_InvoiceIndex(request):
    Status=M_Invoice.InvoiceStatusList
    FeeID=M_FeeItem.objects.all().values_list('FeeID', 'FeeName')
    Station=M_Station.objects.all().values_list('StationID', 'StationName')
    return render(request,'Invoice/index.html',{'FeeID':FeeID,'Status':Status,'Station':Station})


@csrf_protect
def V_GetInvoiceData(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數

    grid=GridCS(request)
    InvoiceData=grid.dynamic_query_order(M_V_Invoice)
    object_list = grid.dynamic_query_order_paginator(InvoiceData)

    count=len(InvoiceData)

    data=[{	'MaxInvoice': Invoice.MaxInvoice,
            'MinInvoice': Invoice.MinInvoice,
            'TotalInvoice': Invoice.TotalInvoice,
            'TotalAmount': Invoice.TotalAmount,
            'StationID': Invoice.StationID,
            'StationName': Invoice.StationName,
            'FeeID': Invoice.FeeID,
            'FeeName': Invoice.FeeName,
            'Status':  [val for key,val in M_Invoice.InvoiceStatusList if key==Invoice.Status]
            } for Invoice in object_list]

    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }
    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')


def V_AddInvoiceData(request):
    if request.method == 'GET':
        form = AddInvoiceForm()
        return render(request, 'Invoice/AddInvoice.html', {'form':form})

    form=AddInvoiceForm(request.POST)
    if form.is_valid():
        i=1
        StartKey=form.cleaned_data['StartInvoiceNo'][:1]
        AddKeyLength=len(form.cleaned_data['StartInvoiceNo'][1:])
        AddKey=int(form.cleaned_data['StartInvoiceNo'][1:])
        FeeItemObject=M_FeeItem.objects.get(pk=form.cleaned_data['FeeID'])
        StationObject=M_Station.objects.get(pk=form.cleaned_data['StationID'])
        LastLotNo=M_Invoice.objects.all().aggregate(Max('LotNo'))
        BulkCreateList=[]
        while i<=form.cleaned_data['AddCount']:
            data=M_Invoice()
            data.FeeID=FeeItemObject
            data.InvoiceNo=StartKey+(("%0"+str(AddKeyLength)+"d") % AddKey)
            data.Status='2'
            data.Amount=FeeItemObject.FeeAmount
            data.StationID=StationObject
            data.LotNo=LastLotNo['LotNo__max']+1
            data.Creator=request.user
            data.CreateDate=datetime.datetime.now()
            BulkCreateList.append(data)
            i=i+1
            AddKey=AddKey+1
        M_Invoice.objects.bulk_create(BulkCreateList,form.cleaned_data['AddCount'])
        messages.success(request, '新增成功!', extra_tags='alert')
        Status=M_Invoice.InvoiceStatusList
        FeeID=M_FeeItem.objects.all().values_list('FeeID', 'FeeName')
        Station=M_Station.objects.all().values_list('StationID', 'StationName')
        return render(request,'Invoice/index.html',{'FeeID':FeeID,'Status':Status,'Station':Station})

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from Invoice.models import M_Invoice,M_V_Invoice
import datetime,json
from CommonApp.models import GridCS
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.
def V_InvoiceIndex(request):
    return render(request,'Invoice/index.html')


@csrf_protect
def V_GetInvoiceData(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數

    grid=GridCS(request)
    InvoiceData=grid.dynamic_query_order(M_V_Invoice)
    object_list = grid.dynamic_query_order_paginator(InvoiceData)

    count=len(InvoiceData)

    data=[{	'InvoiceNo': Invoice.InvoiceNo,
            #'InvoiceNo': Invoice.InvoiceNo,
            #'Amount': Invoice.Amount,
            #'StationID': Invoice.StationID.StationName,
            #'Status':  [val for key,val in M_Invoice.InvoiceStatusList if key==M_Invoice.Status],
            'pk': Invoice.pk} for Invoice in object_list]

    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }
    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from Deal.models import M_DealMaster,M_DealDetail
import datetime,json
from CommonApp.models import GridCS
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.
def V_DealIndex(request):
    return render(request,'Deal/index.html')

@csrf_protect
def V_GetDealMasterData(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數

    grid=GridCS(request)
    MasterData=grid.dynamic_query_order(M_DealMaster)
    object_list = grid.dynamic_query_order_paginator(MasterData)

    count=len(MasterData)

    data=[{	'StationID': Master.StationID.StationName,
            'DealDate': Master.DealDate,
            'Cashier': Master.Cashier.EmployeeName,
            'InvoiceNo': Master.InvoiceNo.InvoiceNo,
            'Amount': Master.Amount,
            'PayType':  [val for key,val in M_DealMaster.PayTypeList if key==Master.PayType],
            'Status':  [val for key,val in M_DealMaster.DealStatusList if key==Master.Status],
            'pk': Master.pk} for Master in object_list]

    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }
    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')



@csrf_protect
def V_GetDealDetailData(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數

    grid=GridCS(request)
    DetailData=grid.dynamic_query_order(M_DealDetail)


    count=len(DetailData)

    data=[{	'FeeID': Detail.FeeID.FeeName,
            'Amount': Detail.Amount,
            'Qty': Detail.Qty,
            'TotalAmount': Detail.TotalAmount,
            'Remark': Detail.Remark,
            'pk': Detail.pk} for Detail in DetailData]

    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }
    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')

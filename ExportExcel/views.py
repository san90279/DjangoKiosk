from django.shortcuts import render
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.views.decorators.csrf import csrf_protect
import os
import datetime,json
from django.http import HttpResponse
from ExportExcel.models import M_V_PenaltyReport,M_V_FeeItemReport
from Deal.models import M_DealMaster
from CommonApp.models import GridCS
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.
def V_DayReportIndex(request):
    if(request.method=='GET'):
        return render(request,'ExportExcel/DayReportIndex.html');
    module_dir = os.path.dirname(__file__)
    path=open(os.path.join(module_dir+'/ExcelTemplate/', '日報表.xlsx'),'rb')
    wb = load_workbook(filename = path)
    wb.template=True
    ws = wb.active
    response = HttpResponse(save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename={0}.xlsx'.format('Export')
    return response


def V_MonthReportIndex(request):
    return render(request,'ExportExcel/MonthReportIndex.html');


def V_PenaltyReportIndex(request):
    return render(request,'ExportExcel/PenaltyReportIndex.html');


def V_FeeItemReportIndex(request):
    Status=M_DealMaster.DealStatusList
    PayType=M_DealMaster.PayTypeList
    return render(request,'ExportExcel/FeeItemReportIndex.html',{'Status':Status,'PayType':PayType});


@csrf_protect
def V_GetPenaltyReport(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數

    grid=GridCS(request)
    PenaltyData=grid.dynamic_query_order(M_V_PenaltyReport)


    count=len(PenaltyData)
    data=[{	'DealDate': Penalty.DealDate.strftime('%Y-%m-%d'),
            'PenaltyID':Penalty.PenaltyID  ,
            'PenaltyName': Penalty.PenaltyName,
            'TermID': Penalty.TermID ,
            'TermName': Penalty.TermName ,
            'Qty': Penalty.qty,
            'TotalAmount': Penalty.totalamount,
            'Remark': Penalty.Remark} for Penalty in PenaltyData]

    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }
    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')


@csrf_protect
def V_GetFeeItemReport(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數

    grid=GridCS(request)
    FeeItemData=grid.dynamic_query_order(M_V_FeeItemReport)
    object_list = grid.dynamic_query_order_paginator(FeeItemData)

    count=len(FeeItemData)
    data=[{	'StationID': FeeItem.StationID,
            'DealDate': FeeItem.DealDate.strftime('%Y-%m-%d'),
            'DealTime': FeeItem.DealDate.strftime('%H:%M:%S'),
            'InvoiceNo':FeeItem.InvoiceNo ,
            'Status': FeeItem.Status,
            'FeeID': FeeItem.FeeID,
            'FeeName': FeeItem.FeeName,
            'Amount': FeeItem.Amount,
            'cAmount': FeeItem.Amount,
            'Qty': FeeItem.Qty} for FeeItem in object_list]

    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }
    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')

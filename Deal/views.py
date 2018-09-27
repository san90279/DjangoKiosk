from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q, Max
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from EmployeeCard.models import M_EmployeeCard
from Store.models import M_Station
from FeeItem.models import M_FeeItem
from Invoice.models import M_Invoice
from Deal.models import M_DealMaster,M_DealDetail,M_V_entry,M_V_DealDetail
import datetime,json
from Deal.forms import EntryForm
from CommonApp.models import GridCS
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
# Create your views here.
def V_DealIndex(request):
    Status=M_DealMaster.DealStatusList
    Cashier=M_EmployeeCard.objects.all().values_list('pk', 'EmployeeName')
    PayType=M_DealMaster.PayTypeList
    FeeID=M_FeeItem.objects.all().values_list('pk', 'FeeName')
    return render(request,'Deal/index.html',{'Cashier':Cashier,'Status':Status,'PayType':PayType,'FeeID':FeeID})

@csrf_protect
def V_GetDealMasterData(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數

    grid=GridCS(request)
    MasterData=grid.dynamic_query_order(M_DealMaster)


    if(request.POST.get('FeeID', '')!=''):
        filterFee=request.POST.get('FeeID', '')
        FeeDetailData=M_DealDetail.objects.filter(FeeID=filterFee).values_list('MasterID')
        MasterData=MasterData.filter(id__in=FeeDetailData)

    object_list = grid.dynamic_query_order_paginator(MasterData)
    count=len(MasterData)

    data=[{	'StationID': Master.StationID.StationName,
            'DealDate': Master.DealDate.strftime("%Y-%m-%d %H:%M"),
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

    data=[{	'FeeID': Detail.FeeID.FeeID,
            'FeeName': Detail.FeeID.FeeName,
            'Amount': Detail.Amount,
            'Qty': Detail.Qty,
            'TotalAmount':Detail.TotalAmount,
            'Remark': Detail.Remark,
            'MasterID': Detail.MasterID.pk} for Detail in DetailData]

    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }
    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')



#-------------------------交易補登------------------------------#
def V_EntryIndex(request):
    #收銀人員項DropDown使用
    EmployeeList= M_EmployeeCard.objects.all().values_list('EmployeeID', 'EmployeeName')
    #站別項DropDown使用
    StationList= M_Station.objects.all().values_list('StationID', 'StationName')
    #規費項DropDown使用
    FeeList= M_FeeItem.objects.all().values_list('FeeID', 'FeeName')
    #付款別項DropDown使用
    PayTypeList=M_V_entry.PayTypeList
    return render(request,'Deal/entry_index.html',{'employee':EmployeeList,'station':StationList,'fee':FeeList,'paytype':PayTypeList})

def V_EntryDelete(request, DealDate,LotNo):
    Mobject=M_DealMaster.objects.filter(Q(DealDate=DealDate,LotNo=LotNo))
    for master in Mobject:
        #更新Invoice 狀態status=2:未使用
        M_Invoice.objects.filter(Q(pk=master.InvoiceNo_id)).update(Status=2)
        #刪除關聯Deatail
        M_DealDetail.objects.filter(Q(MasterID=master.id)).delete()
    #刪除Master
    Mobject.delete()
    #跳轉至首頁
    return redirect('EntryIndex')

def V_EntryNew(request):
    #指定模板路徑
    template = 'Deal/entry_Edit.html'
    if request.method == "POST":
        form = EntryForm(request.POST)
        #判斷必填欄位
        if form.is_valid():
            StationObject=M_Station.objects.get(pk=form.cleaned_data['StationID'])
            MatchObject=M_Invoice.objects.filter(StationID=StationObject)
            Qty=int(form.cleaned_data['Qty'])
            StartKey=form.cleaned_data['beginno'][:1]
            AddKey=int(form.cleaned_data['beginno'][1:])
            InvoiceList=[] #存累加的票據號
            for i in range(0,Qty,1):
                InvoiceList.append(StartKey+str(AddKey+i))
            CheckInvoice=M_Invoice.objects.filter(Q(InvoiceNo__in=InvoiceList,Status=2)).count()
            if MatchObject and CheckInvoice==Qty:
                DealDate=form.cleaned_data['DealDate']
                PayType=form.cleaned_data['PayType']
                EmployeeObject=M_EmployeeCard.objects.get(pk=form.cleaned_data['EmployeeCardID'])
                FeeItemObject=M_FeeItem.objects.get(pk=form.cleaned_data['FeeID'])
                LastLotNo=M_DealMaster.objects.filter(Q(DealDate=DealDate)).aggregate(Max('LotNo'))
                BulkCreateList_m=[]
                BulkCreateList_d=[]
                if LastLotNo['LotNo__max'] is None:
                    lotno=1
                else:
                    lotno=LastLotNo['LotNo__max']+1
                for i in InvoiceList:
                    data_m=M_DealMaster()
                    data_m.StationID=StationObject
                    data_m.DealDate=DealDate
                    data_m.Cashier=EmployeeObject
                    data_m.Amount=FeeItemObject.FeeAmount
                    data_m.PayType=PayType
                    data_m.LotNo=lotno
                    data_m.InvoiceNo=M_Invoice.objects.get(InvoiceNo=i)
                    data_m.IsOutside=True
                    data_m.IsCheckout=False
                    data_m.Creator = request.user
                    data_m.CreateDate = datetime.datetime.now()
                    BulkCreateList_m.append(data_m)
                    AddKey=AddKey+1
                M_DealMaster.objects.bulk_create(BulkCreateList_m,form.cleaned_data['Qty'])

                #查詢該批補登交易master的id值
                DetailObject=M_DealMaster.objects.filter(Q(LotNo=lotno))
                for detail in DetailObject:
                    data_d=M_DealDetail()
                    data_d.MasterID=M_DealMaster.objects.get(pk=detail.id)
                    data_d.FeeID=FeeItemObject
                    data_d.Amount=FeeItemObject.FeeAmount
                    data_d.Qty=1
                    data_d.TotalAmount=FeeItemObject.FeeAmount
                    data_d.Remark=''
                    data_d.Creator = request.user
                    data_d.CreateDate = datetime.datetime.now()
                    BulkCreateList_d.append(data_d)
                M_DealDetail.objects.bulk_create(BulkCreateList_d,form.cleaned_data['Qty'])
                #更新發票狀態為[1:使用]
                MatchObject.update(Status=1)
                messages.success(request, '交易補登成功!', extra_tags='alert')
                return redirect('EntryIndex')
            else :
                messages.error(request, '憑證號碼:{} 無法使用，或者憑證無法對應可使用的站點!'.format(form.cleaned_data['beginno']), extra_tags='alert')
                return render(request, template, {'form': form})
    else:
        form = EntryForm()
    return render(request, template, {'form': form})

@csrf_protect
def V_GetEntryData(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數

    grid=GridCS(request)
    EntryData=grid.dynamic_query_order(M_V_entry)


    count=len(EntryData)
    data=[{	'DealDate': Enrty.DealDate.strftime('%Y-%m-%d'),
            'EmployeeID': Enrty.EmployeeID,
            'StationID': Enrty.StationID,
            'FeeID': Enrty.FeeID,
            'FeeName': Enrty.FeeName,
            'beginno': Enrty.beginno,
            'PayType':[val for key,val in M_DealMaster.PayTypeList if key==Enrty.PayType] ,
            'Amount': Enrty.Amount,
            'Qty': Enrty.Qty,
            'TotalAmount': Enrty.TotalAmount,
            'Status': Enrty.Status,
            'IsCheckout': Enrty.IsCheckout,
            'LotNo': Enrty.LotNo} for Enrty in EntryData]

    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }
    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')

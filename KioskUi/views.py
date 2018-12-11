from django.shortcuts import render
from FeeItem.models import M_FeeItem
from EmployeeCard.models import M_EmployeeCard
from django.http import HttpResponse
from django.contrib.auth.models import User
from Invoice.models import M_Invoice
from Penalty.models import M_Penalty
from Term.models import M_Term
from Store.models import M_Station
from Deal.models import M_DealMaster,M_DealDetail
from django.core.serializers.json import DjangoJSONEncoder
import json,datetime

# Create your views here.
def V_KioskIndex(request):
    return render(request,'KioskUi/index.html')

def V_KioskPick(request,id):
    Feelist=M_FeeItem.objects.filter(Status='1').order_by('OrderBy')
    TermList=M_Term.objects.all()
    PenaltyList=M_Penalty.objects.all()
    UserName=User.objects.get(id=id).last_name
    return render(request,'KioskUi/pick.html',{"Feelist":Feelist,"UserID":id,"TermList":TermList,"PenaltyList":PenaltyList,"UserName":UserName})

def V_GetEmployeeData(request,CardNo):
    try:
        EmployeeData=M_EmployeeCard.objects.get(CardNo=CardNo)
        UserDate=User.objects.get(username=EmployeeData.EmployeeID)
        return HttpResponse(UserDate.id)
    except Exception as e:
        return HttpResponse('')


def V_Refund(request,id):
    return render(request,'KioskUi/Refund.html',{"UserID":id})

def V_GetDealList(request,InvoiceNo):
    DealList=M_DealMaster.objects.filter(InvoiceNo_id__InvoiceNo__icontains=InvoiceNo,Status=1,IsCheckout=False).order_by('InvoiceNo')
    data=[{	'InvoiceNo': deal.InvoiceNo.InvoiceNo,'MasterID':deal.id,'PayType':deal.PayType,'PayTypeName':dict(M_DealMaster.PayTypeList)[deal.PayType]} for deal in DealList]
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

def V_GetDealData(request,MasterID):
    DealData=M_DealDetail.objects.filter(MasterID=MasterID)
    data=[{	'FeeItem': deal.FeeID.FeeName,
            'Amount':deal.Amount,
            'Qty':deal.Qty
            } for deal in DealData]
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

def V_SaveDealData(request,PayType):
    PostJsonStr=request.POST.get('DataJson')
    DataObject=json.loads(PostJsonStr)

    InvoiceData=M_Invoice.objects.filter(FeeID='31',Status='2',StationID='1').order_by("id")[0]
    InvoiceData.Status=1
    InvoiceData.save()

    data_m=M_DealMaster()
    data_m.StationID=M_Station.objects.get(id=1)
    data_m.DealDate=datetime.datetime.now()
    data_m.Status='1'
    data_m.Cashier=User.objects.get(id=DataObject[0]['Cashier'])
    data_m.PayType=PayType
    data_m.LotNo=0
    data_m.Creator=User.objects.get(id=DataObject[0]['Cashier'])
    data_m.CreateDate=datetime.datetime.now()
    data_m.InvoiceNo=InvoiceData
    data_m.Amount=DataObject[0]['TotalAmount']
    data_m.IsCheckout=False
    data_m.IsOutside=False
    data_m.save()

    for detail in DataObject[1:]:
        data_d=M_DealDetail()
        data_d.MasterID=data_m
        data_d.FeeID=M_FeeItem.objects.get(id=detail['Fee'])
        data_d.Amount=detail['Price']
        data_d.Qty=detail['FeeCount']
        data_d.TotalAmount=int(detail['FeeCount'])*int(detail['Price'])
        if(detail['Penalty']!=''):
            data_d.PenaltyID=M_Penalty.objects.get(id=int(detail['Penalty']))
        if(detail['Term']!=''):
            data_d.TermID=M_Term.objects.get(id=int(detail['Term']))
        data_d.Creator=User.objects.get(id=DataObject[0]['Cashier'])
        data_d.CreateDate=datetime.datetime.now()
        data_d.save()

    return HttpResponse(json.dumps({'InvoiceNo':InvoiceData.InvoiceNo,'MasterID':data_m.id}, cls=DjangoJSONEncoder), content_type='application/json')

def V_RefundDealData(request,MasterID,UserID):
    data_m=M_DealMaster.objects.get(id=MasterID)
    data_m.Status='0'
    data_m.Editor=User.objects.get(id=UserID)
    data_m.EditDate=datetime.datetime.now()
    data_m.save()
    return HttpResponse(True)

def V_PrintInvoice(request,MasterID):
    data_m=M_DealMaster.objects.get(id=MasterID)
    data_d=M_DealDetail.objects.filter(MasterID=MasterID)
    TEL=''
    FAX=''
    NumOfReci=''
    ItemAndMoney=''
    TotalMoney=''
    CashOrCard=''
    OP=''
    #KioskDll.EPSON_RECEIPT_PRINT(TEL,FAX,NumOfReci,ItemAndMoney,TotalMoney,CashOrCard,OP)
    return HttpResponse("true")

def V_PayEntry(request,id):
    return render(request,'KioskUi/PayEntry.html',{"UserID":id})

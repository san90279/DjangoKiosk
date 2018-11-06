from django.shortcuts import render
from FeeItem.models import M_FeeItem
from EmployeeCard.models import M_EmployeeCard
from django.http import HttpResponse
from django.contrib.auth.models import User
from Penalty.models import M_Penalty
from Term.models import M_Term
from Deal.models import M_DealMaster,M_DealDetail
from django.core.serializers.json import DjangoJSONEncoder
import json
import clr
clr.AddReference("Household")
from CYP import Household

KioskDll=Household()
# Create your views here.
def V_KioskIndex(request):
    return render(request,'KioskUi/index.html')

def V_KioskPick(request,id):
    Feelist=M_FeeItem.objects.all()
    TermList=M_Term.objects.all()
    PenaltyList=M_Penalty.objects.all()
    return render(request,'KioskUi/pick.html',{"Feelist":Feelist,"UserID":id,"TermList":TermList,"PenaltyList":PenaltyList})

def V_GetEmployeeData(request):
    CardNo=KioskDll.NFC_GETUID(30)
    try:
        EmployeeData=M_EmployeeCard.objects.get(CardNo=CardNo)
        UserDate=User.objects.get(username=EmployeeData.EmployeeID)
        return HttpResponse(UserDate.id)
    except Exception as e:
        return HttpResponse('')


def V_Refund(request,id):
    return render(request,'KioskUi/Refund.html',{"UserID":id})

def V_GetDealList(request,InvoiceNo):
    DealList=M_DealMaster.objects.filter(InvoiceNo_id__InvoiceNo__icontains=InvoiceNo).order_by('InvoiceNo')
    data=[{	'InvoiceNo': deal.InvoiceNo.InvoiceNo,'MasterID':deal.id} for deal in DealList]
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

def V_GetDealData(request,MasterID):
    DealData=M_DealDetail.objects.filter(MasterID=MasterID)
    data=[{	'FeeItem': deal.FeeID.FeeName,
            'Amount':deal.Amount,
            'Qty':deal.Qty
            } for deal in DealData]
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

def V_ConnectKioskPay(request):
    #退幣機
    KioskDll.Hopper_Connect()
    #紙鈔機
    KioskDll.NV11_INITS1()
    #收幣機
    KioskDll.Slot_Connect()
    return HttpResponse("true")
def V_ConnectKioskRefund(request):
    #退幣機
    KioskDll.Hopper_Connect()
    return HttpResponse("true")

def V_SendHowMuchPay(request,Amount):
    KioskDll.SetPrice(Amount)
    return HttpResponse("true")

def V_CheckHowMuchPay(request):
    AmountJson=KioskDll.GetMoney()
    AmountData = json.loads(AmountJson)
    return HttpResponse(AmountData['TotalMoney'])

def V_PrintInvoiceNo(request,InvoiceNo):
    KioskDll.EPSON_SERIAL_PRINT(InvoiceNo)
    return HttpResponse("true")

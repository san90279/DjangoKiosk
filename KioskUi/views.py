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

# Create your views here.
def V_KioskIndex(request):
    return render(request,'KioskUi/index.html')

def V_KioskPick(request,id):
    Feelist=M_FeeItem.objects.all()
    TermList=M_Term.objects.all()
    PenaltyList=M_Penalty.objects.all()
    return render(request,'KioskUi/pick.html',{"Feelist":Feelist,"UserID":id,"TermList":TermList,"PenaltyList":PenaltyList})

def V_GetEmployeeData(request):
    CardNo='9876543210'
    EmployeeData=M_EmployeeCard.objects.get(CardNo=CardNo)
    UserDate=User.objects.get(username=EmployeeData.EmployeeID)
    return HttpResponse(UserDate.id)

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
from django.shortcuts import render
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
import json
#import clr
#clr.AddReference("Household")
#from CYP import Household
#KioskDll=Household()
# Create your views here.
def V_ReserveIndex(request):
    return render(request,'Reserve/index.html')

#def V_ReserveData(request):
    #feedback=KioskDll.GetMoney_Cashbox()
    #data =[json.load(feedback)]
    #return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

#def V_ReserveSetzero(request):
    #zero=KioskDll.Money_Set_Zero()
    #if zero==True:
        #messages.success(request, '成功歸零所有幣別計數!', extra_tags='alert')
    #return render(request,'Reserve/index.html')

#def V_ReserveSetmoney(request,count):
    #flag=KioskDll.Hopper_SetCoinLevels(count)
    #if flag==True:
        #messages.success(request, '成功設定各硬幣別的數量!', extra_tags='alert')
    #return render(request,'Reserve/index.html')

#def V_ReserveReturn(request):
    #jstr=KioskDll.Hopper_SmartEmpty()
    #if jstr:
        #data=json.load(jstr)
        #messages.success(request, '成功清空硬幣!1元{}個,5元{}個,10元{}個,50元{}個'.format(data[0],data[1],data[2],data[3]), extra_tags='alert')
    #return render(request,'Reserve/index.html')

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from Checkout.models import M_Checkout
from Deal.models import M_DealMaster
from django.db.models import Q
import datetime,json
from CommonApp.models import GridCS
from Checkout.forms import CheckoutForm
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
# Create your views here.
def V_CheckoutIndex(request):
    return render(request,'Checkout/index.html')


@csrf_protect
def V_GetCheckoutData(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數
    #將前端request物件傳入GridCS內做處理
    grid=GridCS(request)
    #將Model M_Checkout傳入作查詢
    CheckoutData=grid.dynamic_query_order(M_Checkout)
    #將CheckoutData資料作後端分頁
    object_list = grid.dynamic_query_order_paginator(CheckoutData)
    #資料總筆數
    count=len(CheckoutData)
    #拼出teplate JQGRID 欄位JSON資料流
    data=[{	'CloseDate': Checkout.CloseDate,
            'Editor':Checkout.Editor.username,
            'RecordTime':Checkout.RecordTime.strftime('%Y-%m-%d %H:%M:%S'),
            'pk': Checkout.pk} for Checkout in object_list]
    #JQGRID API
    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }
    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')

def V_CheckoutNew(request):
    template = 'Checkout/Checkout.html'
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        #檢查form表單內是否有非法輸入
        if form.is_valid():
            Checkout = form.save(commit=False)
            #更新過帳旗標欄位
            M_DealMaster.objects.filter(Q(DealDate__date=Checkout.CloseDate)).update(IsCheckout=True)
            Checkout.Editor = request.user
            Checkout.RecordTime = datetime.datetime.now()
            Checkout.save()
            messages.success(request, '日期:{} 過帳成功!'.format(Checkout.CloseDate), extra_tags='alert')
            return redirect('CheckoutIndex')
    else:
        form = CheckoutForm()
    return render(request, template, {'form': form})

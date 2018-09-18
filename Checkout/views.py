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

    grid=GridCS(request)
    CheckoutData=grid.dynamic_query_order(M_Checkout)
    object_list = grid.dynamic_query_order_paginator(CheckoutData)

    count=len(CheckoutData)

    data=[{	'CloseDate': Checkout.CloseDate,
            'Editor':Checkout.Editor.username,
            'RecordTime':Checkout.RecordTime.strftime('%Y-%m-%d %H:%M:%S'),
            'pk': Checkout.pk} for Checkout in object_list]

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
        if form.is_valid():
            Checkout = form.save(commit=False)
            M_DealMaster.objects.filter(Q(DealDate__lte=Checkout.CloseDate)).update(IsCheckout=True)
            Checkout.Editor = request.user
            Checkout.RecordTime = datetime.datetime.now()
            Checkout.save()
            messages.success(request, '日期:{} 過帳成功!'.format(Checkout.CloseDate), extra_tags='alert')
            return redirect('CheckoutIndex')
    else:
        form = CheckoutForm()
    return render(request, template, {'form': form})

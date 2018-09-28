from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query_utils import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect
from FeeItem.forms import FeeItemForm
from FeeItem.models import M_FeeItem
import datetime,json
from CommonApp.models import GridCS
from django.contrib import messages
#規費主頁
def V_FeeItemIndex(request):
    type=M_FeeItem.FeeTypeList
    status=M_FeeItem.FeeStatusList

    return render(request,'FeeItem/index.html',{'type':type,'status':status});
#JQGRID取得規費資料
@csrf_protect
def V_GetFeeItemData(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數
    #將前端request物件傳入GridCS內做處理
    grid=GridCS(request)
    #將Model M_FeeItem傳入作查詢
    FeeItemData=grid.dynamic_query_order(M_FeeItem)
    #將FeeItemData傳入作後端分頁
    object_list = grid.dynamic_query_order_paginator(FeeItemData)
    #資料總筆數
    count=len(FeeItemData)
    #拼出teplate JQGRID 欄位JSON資料流
    data=[{	'FeeID': FeeItem.FeeID,
            'FeeName': FeeItem.FeeName,
            'Remark': FeeItem.Remark,
            'FeeAmount': FeeItem.FeeAmount,
            'FeeType':  [val for key,val in M_FeeItem.FeeTypeList if key==FeeItem.FeeType],
            'Status':  [val for key,val in M_FeeItem.FeeStatusList if key==FeeItem.Status],
            'pk': FeeItem.pk} for FeeItem in object_list]
    #JQGRID API
    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }


    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')



#規費編輯
def V_FeeItemEdit(request, id):
    FeeItemData = get_object_or_404(M_FeeItem, pk=id)
    template = 'FeeItem/Edit.html'
    if request.method == 'GET':
        form = FeeItemForm(instance=FeeItemData)
        return render(request, template, {'form':form})

    # POST
    form = FeeItemForm(request.POST, instance=FeeItemData)
    if not form.is_valid():
        return render(request, template, {'form':form})
    else:
        FeeItem = form.save(commit=False)
        FeeItem.Editor = request.user
        FeeItem.EditDate = datetime.datetime.now()
        FeeItem.save()
        messages.success(request, '規費項目編輯成功!', extra_tags='alert')
        return redirect('FeeItemIndex')
#規費新增
def V_FeeItemNew(request):
    template = 'FeeItem/Edit.html'
    if request.method == "POST":
        form = FeeItemForm(request.POST)
        if form.is_valid():
            FeeItem = form.save(commit=False)
            FeeItem.Editor = request.user
            FeeItem.EditDate = datetime.datetime.now()
            FeeItem.save()
            messages.success(request, '規費項目新增成功!', extra_tags='alert')
            return redirect('FeeItemIndex')
    else:
        form = FeeItemForm()
    return render(request, template, {'form': form})

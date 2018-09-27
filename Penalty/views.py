from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query_utils import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect
from Penalty.forms import PenaltyForm
from Penalty.models import M_Penalty
import datetime,json
from CommonApp.models import GridCS

#罰緩主頁
def V_PenaltyIndex(request):
    return render(request,'Penalty/index.html');

#JQGRID取得罰緩資料
@csrf_protect
def V_GetPenaltyData(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數
    #將前端request物件傳入GridCS內做處理
    grid=GridCS(request)
    #將Model M_Penalty傳入作查詢
    PenaltyData=grid.dynamic_query_order(M_Penalty)
    #將PenaltyData傳入作後端分頁
    object_list = grid.dynamic_query_order_paginator(PenaltyData)
    #資料總筆數
    count=len(PenaltyData)
    #拼出teplate JQGRID 欄位JSON資料流
    data=[{	'PenaltyID': penalty.PenaltyID,
			'PenaltyName': penalty.PenaltyName,
			'Remark': penalty.Remark,
            'pk': penalty.pk} for penalty in object_list]
    #JQGRID API
    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }
    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')



#罰緩編輯
def V_PenaltyEdit(request, id):
    PenaltyData = get_object_or_404(M_Penalty, pk=id)
    template = 'Penalty/Edit.html'
    if request.method == 'GET':
        form = PenaltyForm(instance=PenaltyData)
        return render(request, template, {'form':form})

    # POST
    form = PenaltyForm(request.POST, instance=PenaltyData)
    if not form.is_valid():
        return render(request, template, {'form':form})
    else:
        Penalty = form.save(commit=False)
        Penalty.Editor = request.user
        Penalty.EditDate = datetime.datetime.now()
        Penalty.save()
        return redirect('PenaltyIndex')

        
#罰緩新增
def V_PenaltyNew(request):
    template = 'Penalty/Edit.html'
    if request.method == "POST":
        form = PenaltyForm(request.POST)
        if form.is_valid():
            Penalty = form.save(commit=False)
            Penalty.Editor = request.user
            Penalty.EditDate = datetime.datetime.now()
            Penalty.save()
            return redirect('PenaltyIndex')
    else:
        form = PenaltyForm()
    return render(request, template, {'form': form})

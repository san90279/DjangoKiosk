from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query_utils import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect
from Store.forms import StoreForm,StationForm
from Store.models import M_Store,M_Station,M_V_Station
import datetime,json
from CommonApp.models import GridCS

#站點主頁
def V_StationIndex(request):
    return render(request,'Store/index.html');

#戶所站點JQGRID資料取得
@csrf_protect
def V_GetStationData(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數
    #將前端request物件傳入GridCS內做處理
    grid=GridCS(request)
    #將Model M_V_Station傳入作查詢
    StoreData=grid.dynamic_query_order(M_V_Station)
    #將StoreData傳入作後端分頁
    object_list = grid.dynamic_query_order_paginator(StoreData)
    #資料總筆數
    count=len(StoreData)
    #拼出teplate JQGRID 欄位JSON資料流
    data=[{	'StoreID': Store.StoreID,
            'StoreName': Store.StoreName,
            'StationID': Store.StationID,
            'StationName': Store.StationName,
            'pk': Store.pk} for Store in object_list]
    #JQGRID API
    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }


    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')



#站點編輯
def V_StationEdit(request, id):
    StationData = get_object_or_404(M_Station, pk=id)
    template = 'Store/StationEdit.html'
    if request.method == 'GET':
        form = StationForm(instance=StationData)
        return render(request, template, {'form':form})

    # POST
    form = StationForm(request.POST, instance=StationData)
    if not form.is_valid():
        return render(request, template, {'form':form})
    else:
        Station = form.save(commit=False)
        Station.Editor = request.user
        Station.EditDate = datetime.datetime.now()
        Station.save()
        return redirect('StationIndex')

#戶所新增
def V_StoreNew(request):
    template = 'Store/StoreEdit.html'
    if request.method == "POST":
        form = StoreForm(request.POST)
        if form.is_valid():
            Store = form.save(commit=False)
            Store.Editor = request.user
            Store.EditDate = datetime.datetime.now()
            Store.save()
            return redirect('StationIndex')
    else:
        form = StoreForm()
    return render(request, template, {'form': form})

#站點新增
def V_StationNew(request):
    template = 'Store/StationEdit.html'
    if request.method == "POST":
        form = StationForm(request.POST)
        if form.is_valid():
            Station = form.save(commit=False)
            Station.Editor = request.user
            Station.EditDate = datetime.datetime.now()
            Station.save()
            return redirect('StationIndex')
    else:
        form = StationForm()
    return render(request, template, {'form': form})

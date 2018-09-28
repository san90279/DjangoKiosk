from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from .forms import TermForm
from .models import M_Term
import datetime,json
from django.views.decorators.csrf import csrf_protect
from CommonApp.models import GridCS
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages

# Create your views here.
#條款主頁
def V_TermIndex(request):
    return render(request,'Term/index.html')

#條款JQGRID資料取得
@csrf_protect
def V_GetTermData(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數
    #將前端request物件傳入GridCS內做處理
    grid=GridCS(request)
    #將Model M_Term傳入作查詢
    TermData=grid.dynamic_query_order(M_Term)
    #將TermData傳入作後端分頁
    object_list = grid.dynamic_query_order_paginator(TermData)
    #資料總筆數
    count=len(TermData)
    #拼出teplate JQGRID 欄位JSON資料流
    data=[{	'TermID': term.TermID,
			'TermName': term.TermName,
			'Remark': term.Remark,
            'pk': term.pk} for term in object_list]
    #JQGRID API
    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }
    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')

#條款編輯
def V_TermEdit(request,id=0):
    if(id==0):
        TermData=M_Term()
    else:
        TermData=M_Term.objects.get(pk=id)

    if(request.method == 'GET'):
        form =TermForm(instance=TermData)
        return render(request,'Term/Edit.html',{'form': form});
    else:
        form = TermForm(request.POST,instance=TermData)
        if form.is_valid():
            trems=form.save(commit=False)
            trems.Editor=request.user
            trems.EditDate=datetime.datetime.now()
            trems.save()
            messages.success(request, '儲存成功!', extra_tags='alert')
            return render(request,'Term/index.html')
        else:
            return render(request,'Term/Edit.html',{'form': form});

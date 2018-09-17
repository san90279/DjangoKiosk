from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from .forms import TermForm
from .models import M_Term
import datetime,json
from django.views.decorators.csrf import csrf_protect
from CommonApp.models import GridCS
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def V_TermIndex(request):
    return render(request,'Term/index.html')

@csrf_protect
def V_GetTermData(request):
    draw = int(request.POST.get('draw'))  # 記錄操作次數

    grid=GridCS(request)
    TermData=grid.dynamic_query_order(M_Term)
    object_list = grid.dynamic_query_order_paginator(TermData)

    count=len(TermData)

    data=[{	'TermID': term.TermID,
			'TermName': term.TermName,
			'Remark': term.Remark,
            'pk': term.pk} for term in object_list]
    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }
    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')

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
            return render(request,'Term/index.html')
        else:
            return render(request,'Term/Edit.html',{'form': form});

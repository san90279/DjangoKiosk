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

def V_PenaltyIndex(request):
    return render(request,'Penalty/index.html');

@csrf_protect
def V_GetPenaltyData(request):
    searchPenaltyID = request.POST.get('searchPenaltyID')
    searchPenaltyName = request.POST.get('searchPenaltyName')
    draw = int(request.POST.get('draw'))  # 記錄操作次數
    start = int(request.POST.get('start'))  # 起始位置
    length = int(request.POST.get('length'))  # 每頁長度
    order_column = request.POST.get('order[0][column]')  # 排序字段索引
    order_column = request.POST.get('order[0][dir]')  #排序規則：ase/desc
    try:
        if searchPenaltyID or searchPenaltyName :
            if order_column=='asc':
                PenaltyData = M_Penalty.objects.filter(Q(PenaltyID__icontains=searchPenaltyID) ,
                                              Q(PenaltyName__icontains=searchPenaltyName)).order_by('id')
            else:
                PenaltyData = M_Penalty.objects.filter(Q(PenaltyID__icontains=searchPenaltyID) ,
                                              Q(PenaltyName__icontains=searchPenaltyName)).order_by('-id')
        else:
            if order_column=='asc':
                PenaltyData=M_Penalty.objects.all().order_by('id')
            else:
                PenaltyData=M_Penalty.objects.all().order_by('-id')
    except:
        PenaltyData=None


    paginator = Paginator(PenaltyData, length)
    count=paginator.count
    try:
        object_list = paginator.page(start/length+1).object_list
    except EmptyPage:
        object_list = None

    data=[{	'PenaltyID': penalty.PenaltyID,
			'PenaltyName': penalty.PenaltyName,
			'Remark': penalty.Remark,
            'pk': penalty.pk} for penalty in object_list]
    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }
    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')




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

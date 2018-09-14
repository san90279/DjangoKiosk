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

def V_FeeItemIndex(request):
    type=M_FeeItem.FeeTypeList
    status=M_FeeItem.FeeStatusList
    return render(request,'FeeItem/index.html',{'type':type,'status':status});

@csrf_protect
def V_GetFeeItemData(request):
    searchFeeID = request.POST.get('searchFeeID')
    searchFeeName = request.POST.get('searchFeeName')
    searchRemark = request.POST.get('searchRemark')
    searchFeeType = request.POST.get('searchFeeType')
    searchStatus = request.POST.get('searchStatus')

    draw = int(request.POST.get('draw'))  # 記錄操作次數
    start = int(request.POST.get('start'))  # 起始位置
    length = int(request.POST.get('length'))  # 每頁長度
    search_key = request.POST.get('search[value]')  # 搜索關鍵字
    order_column = request.POST.get('order[0][column]')  # 排序字段索引
    order_column = request.POST.get('order[0][dir]')  #排序規則：ase/desc
    try:
        if searchFeeID or searchFeeName or searchRemark or searchFeeType or searchStatus :
            if order_column=='asc':
                FeeItemData = M_FeeItem.objects.filter(Q(FeeID__icontains=searchFeeID) ,
                                                       Q(FeeName__icontains=searchFeeName) ,
                                                       Q(Remark__icontains=searchRemark) ,
                                                       Q(FeeType__icontains=searchFeeType) ,
                                                       Q(Status__icontains=searchStatus)).order_by('id')
            else:
                FeeItemData = M_FeeItem.objects.filter(Q(FeeID__icontains=searchFeeID) ,
                                                       Q(FeeName__icontains=searchFeeName) ,
                                                       Q(Remark__icontains=searchRemark) ,
                                                       Q(FeeType__icontains=searchFeeType) ,
                                                       Q(Status__icontains=searchStatus)).order_by('-id')
        else:
            if order_column=='asc':
                FeeItemData=M_FeeItem.objects.all().order_by('id')
            else:
                FeeItemData=M_FeeItem.objects.all().order_by('-id')
    except:
        FeeItemData=None
    try:
        count=int(FeeItemData.count())
    except:
        count=0
        length=0
    paginator = Paginator(FeeItemData, length)
    try:
        object_list = paginator.page(start/length+1).object_list
    except :
        object_list =''

    data=[{	'FeeID': FeeItem.FeeID,
            'FeeName': FeeItem.FeeName,
            'Remark': FeeItem.Remark,
            'FeeAmount': FeeItem.FeeAmount,
    'FeeType':  [val for key,val in M_FeeItem.FeeTypeList if key==FeeItem.FeeType],
            'Status':  [val for key,val in M_FeeItem.FeeStatusList if key==FeeItem.Status],
            'pk': FeeItem.pk} for FeeItem in object_list]

    dic = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': data,
    }


    return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), content_type='application/json')




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
        return redirect('FeeItemIndex')

def V_FeeItemNew(request):
    template = 'FeeItem/Edit.html'
    if request.method == "POST":
        form = FeeItemForm(request.POST)
        if form.is_valid():
            FeeItem = form.save(commit=False)
            FeeItem.Editor = request.user
            FeeItem.EditDate = datetime.datetime.now()
            FeeItem.save()
            return redirect('FeeItemIndex')
    else:
        form = FeeItemForm()
    return render(request, template, {'form': form})

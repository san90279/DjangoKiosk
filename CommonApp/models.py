from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
# Create your models here.
class GridCS():
    def __init__(self,request):
        self.SearchFields={}

        i=0
        self.columnList =[]
        while True:
            if request.POST.get('columns[%s][data]' % i):
                self.columnList.extend([request.POST.get('columns[%s][data]' % i)])
                i=i+1
            else:
                break

        for key, value in request.POST.items():
            if(key.startswith(tuple(self.columnList)) and key.find('__')):
                self.SearchFields[key]=value

        self.orderIndex=request.POST.get('order[0][column]')
        self.orderDir = request.POST.get('order[0][dir]')
        self.orderColumn=request.POST.get('columns[%s][data]' % self.orderIndex)
        if(self.orderDir!='asc'):
            self.orderColumn='-'+self.orderColumn

        self.start = int(request.POST.get('start'))  # 起始位置
        self.length = int(request.POST.get('length'))  # 每頁長度

    def dynamic_query(self,model):

        queries = []
        for (f, v) in self.SearchFields.items():
            if v != "":
                kwargs = {str('%s' % f) : str('%s' % v)}
                queries.append(Q(**kwargs))

        if len(queries) > 0:
            q = Q()
            for query in queries:
                q = q & query
            if q:
                data= model.objects.filter(q)
        else:
            data= model.objects.all()

        return data

    def dynamic_query_order(self,model):
        return self.dynamic_query(model).order_by(self.orderColumn)

    def dynamic_query_order_paginatorByModel(self,model):
        data=self.dynamic_query_order(model)
        paginator = Paginator(data, self.length)
        object_list = paginator.page(self.start/self.length+1).object_list
        return object_list

    def dynamic_query_order_paginator(self,data):
        paginator = Paginator(data, self.length)
        object_list = paginator.page(self.start/self.length+1).object_list
        return object_list

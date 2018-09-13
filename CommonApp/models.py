from django.db import models
from django.db.models import Q
# Create your models here.
class GridCS():
    def __init__(self,request):
        i=0
        self.columnList =[]
        while True:
            if request.POST.get('columns[%s][data]' % i):
                self.columnList.extend([request.POST.get('columns[%s][data]' % i)])
                i=i+1
            else:
                break

        self.orderIndex=request.POST.get('order[0][column]')
        self.orderDir = request.POST.get('order[0][dir]')
        self.orderColumn=request.POST.get('columns[%s][data]' % self.orderIndex)

    def dynamic_query(model, fields, types, values, operator):

        queries = []
        for (f, t, v) in zip(fields, types, values):
            if v != "":
                kwargs = {str('%s__%s' % (f,t)) : str('%s' % v)}
                queries.append(Q(**kwargs))

        if len(queries) > 0:
            q = Q()
            for query in queries:
                if operator == "and":
                    q = q & query
                elif operator == "or":
                    q = q | query
                else:
                    q = None
            if q:
                return model.objects.filter(q)
        else:
            return {}

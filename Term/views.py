from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from .forms import TermForm
from .models import M_Term
import datetime

# Create your views here.
def V_TermIndex(request):
    return render(request,'Term/index.html')

def V_GetTermData(request):
    try:
        TermData=M_Term.objects.all()
    except:
        TermData=''
    TermDataJson = serializers.serialize('json', TermData)
    return HttpResponse(TermDataJson, content_type='application/json')

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

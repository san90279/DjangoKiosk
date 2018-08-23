from django.shortcuts import render
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

def V_TermEdit(request,id):
    if(id==0):
        TermData=None
    else:
        TermData=M_Term.objects.get(pk=id)
    form =TermForm(instance=TermData)
    return render(request,'Term/Edit.html',{'form': form});

def V_TremSave(request):
    form = TermForm(request.POST,instance=M_Term)
    if form.is_valid():
        trems=form.save(commit=False)
        trems.Editor=request.user
        trems.EditDate=datetime.datetime.now()
        trems.save()
    else:
        return render(request,'Term/Edit.html',{'form': form});

    return render(request,'Term/index.html')

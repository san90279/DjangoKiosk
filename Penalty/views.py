from django.shortcuts import render, get_object_or_404,redirect
from django.shortcuts import render
from django.http import HttpResponse
from Penalty.models import M_Penalty
from django.core import serializers
from Penalty.forms import PenaltyForm
import datetime

def V_PenaltyIndex(request):
    return render(request,'Penalty/index.html');


def V_GetPenaltyData(request):
    try:
        PenaltyData=M_Penalty.objects.all()
    except:
        PenaltyData=None
    PenaltyDataJson = serializers.serialize('json', PenaltyData)
    return HttpResponse(PenaltyDataJson, content_type='application/json')


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

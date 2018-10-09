from django.shortcuts import render
from FeeItem.models import M_FeeItem
# Create your views here.
def V_KioskIndex(request):
    return render(request,'KioskUi/index.html')

def V_KioskPick(request):
    Feelist=M_FeeItem.objects.all()
    return render(request,'KioskUi/pick.html',{"Feelist":Feelist})

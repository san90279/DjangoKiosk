from django.shortcuts import render

# Create your views here.
def V_EmployeeCardIndex(request):
    return render(request,'EmployeeCard/index.html');

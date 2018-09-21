from django.shortcuts import render
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook
import os
from django.http import HttpResponse

# Create your views here.
def V_DayReportIndex(request):
    if(request.method=='GET'):
        return render(request,'ExportExcel/DayReportIndex.html');
    module_dir = os.path.dirname(__file__)
    path=open(os.path.join(module_dir+'/ExcelTemplate/', '日報表.xlsx'),'rb')
    wb = load_workbook(filename = path)
    wb.template=True
    ws = wb.active
    response = HttpResponse(save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename={0}.xlsx'.format('Export')
    return response




def V_MonthReportIndex(request):
    return render(request,'ExportExcel/MonthReportIndex.html');

from django.shortcuts import render
from io import BytesIO
from openpyxl import load_workbook
import os


# Create your views here.
def V_DayReportIndex(request):
    if(request.method=='GET'):
        return render(request,'ExportExcel/DayReportIndex.html');
    module_dir = os.path.dirname(__file__)
    path=open(os.path.join(module_dir+'/ExcelTemplate/', '日報表.xlsx'))

    wb = load_workbook(filename = path)
    ws = wb.active
    response = HttpResponse(save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename={0}.xlsx'.format('Export')
    response.write(output.getvalue())   # 獲取緩衝區當中的值
    return response




def V_MonthReportIndex(request):
    return render(request,'ExportExcel/MonthReportIndex.html');

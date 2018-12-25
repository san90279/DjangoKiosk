from django.db import models
from django.db.models import Sum
from Deal.models import M_DealMaster
from FeeItem.models import M_FeeItem
import datetime
from copy import copy

# Create your models here.
class M_V_DayReport(models.Model):
    DealDate=models.DateField()
    Status=models.CharField(max_length=10,choices=M_DealMaster.DealStatusList)
    PayType=models.CharField(max_length=10,choices=M_DealMaster.PayTypeList)
    FeeID_id=models.IntegerField()
    FeeID=models.CharField(max_length=10)
    FeeName=models.CharField(max_length=50)
    Amount=models.IntegerField()
    RowCount=models.IntegerField()
    IsOutside=models.BooleanField()
    class Meta:
        managed = False
        db_table = "ExportExcel_M_V_DayReport"

class M_V_MonthReport(models.Model):
    DealDateYear=models.IntegerField()
    DealDateMonth=models.IntegerField()
    Status=models.CharField(max_length=10,choices=M_DealMaster.DealStatusList)
    PayType=models.CharField(max_length=10,choices=M_DealMaster.PayTypeList)
    FeeID_id=models.IntegerField()
    FeeID=models.CharField(max_length=10)
    FeeName=models.CharField(max_length=50)
    Amount=models.IntegerField()
    RowCount=models.IntegerField()
    IsOutside=models.BooleanField()
    class Meta:
        managed = False
        db_table = "ExportExcel_M_V_MonthReport"

class M_V_PenaltyReport(models.Model):

    DealDate=models.DateTimeField()
    PenaltyID=models.CharField(max_length=10)
    PenaltyName=models.CharField(max_length=50)
    TermID=models.CharField(max_length=10)
    TermName=models.CharField(max_length=50)
    qty=models.IntegerField()
    totalamount=models.IntegerField()
    Remark=models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = "ExportExcel_M_V_PenaltyReport"

class M_V_FeeItemReport(models.Model):
    DealDate=models.DateTimeField()
    StationID=models.CharField(max_length=10)
    InvoiceNo=models.CharField(max_length=20)
    PayType=models.CharField(max_length=10,choices=M_DealMaster.PayTypeList)
    Status=models.CharField(max_length=10,choices=M_DealMaster.DealStatusList)
    FeeID=models.CharField(max_length=10)
    FeeName=models.CharField(max_length=50)
    Qty=models.IntegerField()
    Amount=models.IntegerField()
    Remark=models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = "ExportExcel_M_V_FeeItemReport"




def SetReportTitle(ws):
    DefaultCell=ws['P5']
    ws['A4'].border=copy(DefaultCell.border)
    ws['B4'].border=copy(DefaultCell.border)
    ws['E3'].border=copy(DefaultCell.border)
    ws['F3'].border=copy(DefaultCell.border)
    ws['G3'].border=copy(DefaultCell.border)
    ws['I3'].border=copy(DefaultCell.border)
    ws['J3'].border=copy(DefaultCell.border)
    ws['K3'].border=copy(DefaultCell.border)
    ws['M3'].border=copy(DefaultCell.border)
    ws['N3'].border=copy(DefaultCell.border)
    return ws


def SetDayReportExcel(ReportDateS,ReportDateE,ws):
    ws=SetReportTitle(ws)

    if(ReportDateS==''):
        dt=datetime.datetime.now()
    else:
        dt=datetime.datetime.strptime(ReportDateS,'%Y-%m-%d')

    FeeTypeList=M_FeeItem.FeeTypeList
    FeeItemList=M_FeeItem.objects.filter(Status=1).values()
    if(ReportDateE==''):
        ReportDateE=ReportDateS
        ws['K2'] = '{0}年{1}月{2}日填報'.format(dt.year-1911,dt.month,dt.day)
    else:
        dtE=datetime.datetime.strptime(ReportDateE,'%Y-%m-%d')
        ws['K2'] = '{0}年{1}月{2}日-{3}年{4}月{5}日填報'.format(dt.year-1911,dt.month,dt.day,dtE.year-1911,dtE.month,dtE.day)
    DealData=M_V_DayReport.objects.filter(DealDate__range=(datetime.datetime.strptime(ReportDateS,'%Y-%m-%d'),datetime.datetime.strptime(ReportDateE,'%Y-%m-%d'))).values()

    if(len(DealData)==0):
        return None

    #起始的行數
    RowNo=5
    SubTotal=[]
    #預設的style
    DefaultCell=ws['P5']
    for FeeTypeKey,FeeTypeValue in FeeTypeList:
        FeeItemData=FeeItemList.filter(FeeType=FeeTypeKey)
        FeeItemDataCount=len(FeeItemData)
        if (FeeItemDataCount>0):
            ws['A'+str(RowNo)]=FeeTypeValue
            for FeeItem in FeeItemData:
                ws['B'+str(RowNo)]=FeeItem['FeeName']
                ws['B'+str(RowNo)].border=copy(DefaultCell.border)
                ws['B'+str(RowNo)].font=copy(DefaultCell.font)
                ws['C'+str(RowNo)]=FeeItem['FeeAmount']
                ws['C'+str(RowNo)].border=copy(DefaultCell.border)
                ws['C'+str(RowNo)].font=copy(DefaultCell.font)
                #為了merge做準備
                ws['A'+str(RowNo)].border=copy(DefaultCell.border)
                ws['A'+str(RowNo)].font=copy(DefaultCell.font)
                ws['A'+str(RowNo)].alignment =copy(DefaultCell.alignment)
                #塞資料
                RowDate=DealData.filter(FeeID_id=FeeItem['id'])
                ws['D'+str(RowNo)]=RowDate.filter(IsOutside=False, Status=1).aggregate(Sum('RowCount'))['RowCount__sum'] or 0
                ws['D'+str(RowNo)].border=copy(DefaultCell.border)
                ws['D'+str(RowNo)].font=copy(DefaultCell.font)
                ws['E'+str(RowNo)]=RowDate.filter(IsOutside=False, Status=0).aggregate(Sum('RowCount'))['RowCount__sum'] or 0
                ws['E'+str(RowNo)].border=copy(DefaultCell.border)
                ws['E'+str(RowNo)].font=copy(DefaultCell.font)
                ws['F'+str(RowNo)]="=SUM(D{0}:E{0})".format(str(RowNo))
                ws['F'+str(RowNo)].border=copy(DefaultCell.border)
                ws['F'+str(RowNo)].font=copy(DefaultCell.font)
                ws['G'+str(RowNo)]=RowDate.filter(IsOutside=False, Status=1).aggregate(Sum('Amount'))['Amount__sum'] or 0
                ws['G'+str(RowNo)].border=copy(DefaultCell.border)
                ws['G'+str(RowNo)].font=copy(DefaultCell.font)
                ws['H'+str(RowNo)]=RowDate.filter(IsOutside=True, Status=1).aggregate(Sum('RowCount'))['RowCount__sum'] or 0
                ws['H'+str(RowNo)].border=copy(DefaultCell.border)
                ws['H'+str(RowNo)].font=copy(DefaultCell.font)
                ws['I'+str(RowNo)]=RowDate.filter(IsOutside=True, Status=0).aggregate(Sum('RowCount'))['RowCount__sum'] or 0
                ws['I'+str(RowNo)].border=copy(DefaultCell.border)
                ws['I'+str(RowNo)].font=copy(DefaultCell.font)
                ws['J'+str(RowNo)]="=SUM(H{0}:I{0})".format(str(RowNo))
                ws['J'+str(RowNo)].border=copy(DefaultCell.border)
                ws['J'+str(RowNo)].font=copy(DefaultCell.font)
                ws['K'+str(RowNo)]=RowDate.filter(IsOutside=True, Status=1).aggregate(Sum('Amount'))['Amount__sum'] or 0
                ws['K'+str(RowNo)].border=copy(DefaultCell.border)
                ws['K'+str(RowNo)].font=copy(DefaultCell.font)
                ws['L'+str(RowNo)]=RowDate.filter(PayType='PT01', Status=1).aggregate(Sum('Amount'))['Amount__sum'] or 0
                ws['L'+str(RowNo)].border=copy(DefaultCell.border)
                ws['L'+str(RowNo)].font=copy(DefaultCell.font)
                ws['M'+str(RowNo)]=RowDate.filter(PayType='PT02', Status=1).aggregate(Sum('Amount'))['Amount__sum'] or 0
                ws['M'+str(RowNo)].border=copy(DefaultCell.border)
                ws['M'+str(RowNo)].font=copy(DefaultCell.font)
                ws['N'+str(RowNo)]="=SUM(L{0}:M{0})".format(str(RowNo))
                ws['N'+str(RowNo)].border=copy(DefaultCell.border)
                ws['N'+str(RowNo)].font=copy(DefaultCell.font)

                RowNo=RowNo+1
            ws.merge_cells('A{0}:A{1}'.format(str(RowNo-FeeItemDataCount),str(RowNo-1)))

            for num in range(RowNo-FeeItemDataCount,RowNo):
                ws['A'+str(num)].border=copy(DefaultCell.border)

            SubTotal.append(RowNo)
            ws['A'+str(RowNo)]='小計'
            ws['A'+str(RowNo)].border=copy(DefaultCell.border)
            ws['A'+str(RowNo)].font=copy(DefaultCell.font)
            ws['B'+str(RowNo)].border=copy(DefaultCell.border)
            ws['B'+str(RowNo)].font=copy(DefaultCell.font)
            ws['C'+str(RowNo)].border=copy(DefaultCell.border)
            ws['C'+str(RowNo)].font=copy(DefaultCell.font)
            #小計資料
            ws['D'+str(RowNo)]='=SUM(D{0}:D{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['D'+str(RowNo)].border=copy(DefaultCell.border)
            ws['D'+str(RowNo)].font=copy(DefaultCell.font)
            ws['E'+str(RowNo)]='=SUM(E{0}:E{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['E'+str(RowNo)].border=copy(DefaultCell.border)
            ws['E'+str(RowNo)].font=copy(DefaultCell.font)
            ws['F'+str(RowNo)]='=SUM(F{0}:F{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['F'+str(RowNo)].border=copy(DefaultCell.border)
            ws['F'+str(RowNo)].font=copy(DefaultCell.font)
            ws['G'+str(RowNo)]='=SUM(G{0}:G{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['G'+str(RowNo)].border=copy(DefaultCell.border)
            ws['G'+str(RowNo)].font=copy(DefaultCell.font)
            ws['H'+str(RowNo)]='=SUM(H{0}:H{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['H'+str(RowNo)].border=copy(DefaultCell.border)
            ws['H'+str(RowNo)].font=copy(DefaultCell.font)
            ws['I'+str(RowNo)]='=SUM(I{0}:I{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['I'+str(RowNo)].border=copy(DefaultCell.border)
            ws['I'+str(RowNo)].font=copy(DefaultCell.font)
            ws['J'+str(RowNo)]='=SUM(J{0}:J{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['J'+str(RowNo)].border=copy(DefaultCell.border)
            ws['J'+str(RowNo)].font=copy(DefaultCell.font)
            ws['K'+str(RowNo)]='=SUM(K{0}:K{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['K'+str(RowNo)].border=copy(DefaultCell.border)
            ws['K'+str(RowNo)].font=copy(DefaultCell.font)
            ws['L'+str(RowNo)]='=SUM(L{0}:L{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['L'+str(RowNo)].border=copy(DefaultCell.border)
            ws['L'+str(RowNo)].font=copy(DefaultCell.font)
            ws['M'+str(RowNo)]='=SUM(M{0}:M{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['M'+str(RowNo)].border=copy(DefaultCell.border)
            ws['M'+str(RowNo)].font=copy(DefaultCell.font)
            ws['N'+str(RowNo)]='=SUM(N{0}:N{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['N'+str(RowNo)].border=copy(DefaultCell.border)
            ws['N'+str(RowNo)].font=copy(DefaultCell.font)

            RowNo=RowNo+1

    ws['A'+str(RowNo)]='總計'
    ws['A'+str(RowNo)].border=copy(DefaultCell.border)
    ws['A'+str(RowNo)].font=copy(DefaultCell.font)
    #總計資料
    ws['B'+str(RowNo)].border=copy(DefaultCell.border)
    ws['B'+str(RowNo)].font=copy(DefaultCell.font)
    ws['C'+str(RowNo)].border=copy(DefaultCell.border)
    ws['C'+str(RowNo)].font=copy(DefaultCell.font)
    SumCellStr=""
    for i in SubTotal:
        SumCellStr=SumCellStr+'{0}'+str(i)+','
    SumCellStr='=SUM('+SumCellStr[:len(SumCellStr)-1]+')'
    ws['D'+str(RowNo)]=SumCellStr.format('D')
    ws['D'+str(RowNo)].border=copy(DefaultCell.border)
    ws['D'+str(RowNo)].font=copy(DefaultCell.font)
    ws['E'+str(RowNo)]=SumCellStr.format('E')
    ws['E'+str(RowNo)].border=copy(DefaultCell.border)
    ws['E'+str(RowNo)].font=copy(DefaultCell.font)
    ws['F'+str(RowNo)]=SumCellStr.format('F')
    ws['F'+str(RowNo)].border=copy(DefaultCell.border)
    ws['F'+str(RowNo)].font=copy(DefaultCell.font)
    ws['G'+str(RowNo)]=SumCellStr.format('G')
    ws['G'+str(RowNo)].border=copy(DefaultCell.border)
    ws['G'+str(RowNo)].font=copy(DefaultCell.font)
    ws['H'+str(RowNo)]=SumCellStr.format('H')
    ws['H'+str(RowNo)].border=copy(DefaultCell.border)
    ws['H'+str(RowNo)].font=copy(DefaultCell.font)
    ws['I'+str(RowNo)]=SumCellStr.format('I')
    ws['I'+str(RowNo)].border=copy(DefaultCell.border)
    ws['I'+str(RowNo)].font=copy(DefaultCell.font)
    ws['J'+str(RowNo)]=SumCellStr.format('J')
    ws['J'+str(RowNo)].border=copy(DefaultCell.border)
    ws['J'+str(RowNo)].font=copy(DefaultCell.font)
    ws['K'+str(RowNo)]=SumCellStr.format('K')
    ws['K'+str(RowNo)].border=copy(DefaultCell.border)
    ws['K'+str(RowNo)].font=copy(DefaultCell.font)
    ws['L'+str(RowNo)]=SumCellStr.format('L')
    ws['L'+str(RowNo)].border=copy(DefaultCell.border)
    ws['L'+str(RowNo)].font=copy(DefaultCell.font)
    ws['M'+str(RowNo)]=SumCellStr.format('M')
    ws['M'+str(RowNo)].border=copy(DefaultCell.border)
    ws['M'+str(RowNo)].font=copy(DefaultCell.font)
    ws['N'+str(RowNo)]=SumCellStr.format('N')
    ws['N'+str(RowNo)].border=copy(DefaultCell.border)
    ws['N'+str(RowNo)].font=copy(DefaultCell.font)

    RowNo=RowNo+1
    ws['A'+str(RowNo)]='製表人'
    ws['C'+str(RowNo)]='出納'
    ws['F'+str(RowNo)]='業務主管'
    ws['I'+str(RowNo)]='主辦會計'
    ws['L'+str(RowNo)]='機關首長'

    return ws

def SetMonthReportExcel(ReportYear,ReportMonth,ws):
    ws=SetReportTitle(ws)

    ws['K2'] = '{0}年{1}月填報'.format(ReportYear,ReportMonth)

    FeeTypeList=M_FeeItem.FeeTypeList
    FeeItemList=M_FeeItem.objects.filter(Status=1).values()

    DealData=M_V_MonthReport.objects.filter(DealDateYear=ReportYear,DealDateMonth=ReportMonth).values()

    if(len(DealData)==0):
        return None

    #起始的行數
    RowNo=5
    SubTotal=[]
    #預設的style
    DefaultCell=ws['P5']
    for FeeTypeKey,FeeTypeValue in FeeTypeList:
        FeeItemData=FeeItemList.filter(FeeType=FeeTypeKey)
        FeeItemDataCount=len(FeeItemData)
        if (FeeItemDataCount>0):
            ws['A'+str(RowNo)]=FeeTypeValue
            for FeeItem in FeeItemData:
                ws['B'+str(RowNo)]=FeeItem['FeeName']
                ws['B'+str(RowNo)].border=copy(DefaultCell.border)
                ws['B'+str(RowNo)].font=copy(DefaultCell.font)
                ws['C'+str(RowNo)]=FeeItem['FeeAmount']
                ws['C'+str(RowNo)].border=copy(DefaultCell.border)
                ws['C'+str(RowNo)].font=copy(DefaultCell.font)
                #為了merge做準備
                ws['A'+str(RowNo)].border=copy(DefaultCell.border)
                ws['A'+str(RowNo)].font=copy(DefaultCell.font)
                ws['A'+str(RowNo)].alignment =copy(DefaultCell.alignment)
                #塞資料
                RowDate=DealData.filter(FeeID_id=FeeItem['id'])
                ws['D'+str(RowNo)]=RowDate.filter(IsOutside=False, Status=1).aggregate(Sum('RowCount'))['RowCount__sum'] or 0
                ws['D'+str(RowNo)].border=copy(DefaultCell.border)
                ws['D'+str(RowNo)].font=copy(DefaultCell.font)
                ws['E'+str(RowNo)]=RowDate.filter(IsOutside=False, Status=0).aggregate(Sum('RowCount'))['RowCount__sum'] or 0
                ws['E'+str(RowNo)].border=copy(DefaultCell.border)
                ws['E'+str(RowNo)].font=copy(DefaultCell.font)
                ws['G'+str(RowNo)]=RowDate.filter(IsOutside=False, Status=1).aggregate(Sum('Amount'))['Amount__sum'] or 0
                ws['G'+str(RowNo)].border=copy(DefaultCell.border)
                ws['G'+str(RowNo)].font=copy(DefaultCell.font)
                ws['H'+str(RowNo)]=RowDate.filter(IsOutside=True, Status=1).aggregate(Sum('RowCount'))['RowCount__sum'] or 0
                ws['H'+str(RowNo)].border=copy(DefaultCell.border)
                ws['H'+str(RowNo)].font=copy(DefaultCell.font)
                ws['I'+str(RowNo)]=RowDate.filter(IsOutside=True, Status=0).aggregate(Sum('RowCount'))['RowCount__sum'] or 0
                ws['I'+str(RowNo)].border=copy(DefaultCell.border)
                ws['I'+str(RowNo)].font=copy(DefaultCell.font)
                ws['K'+str(RowNo)]=RowDate.filter(IsOutside=True, Status=1).aggregate(Sum('Amount'))['Amount__sum'] or 0
                ws['K'+str(RowNo)].border=copy(DefaultCell.border)
                ws['K'+str(RowNo)].font=copy(DefaultCell.font)
                ws['L'+str(RowNo)]=RowDate.filter(PayType='PT01', Status=1).aggregate(Sum('Amount'))['Amount__sum'] or 0
                ws['L'+str(RowNo)].border=copy(DefaultCell.border)
                ws['L'+str(RowNo)].font=copy(DefaultCell.font)
                ws['M'+str(RowNo)]=RowDate.filter(PayType='PT02', Status=1).aggregate(Sum('Amount'))['Amount__sum'] or 0
                ws['M'+str(RowNo)].border=copy(DefaultCell.border)
                ws['M'+str(RowNo)].font=copy(DefaultCell.font)

                ws['F'+str(RowNo)]="=SUM(D{0}:E{0})".format(str(RowNo))
                ws['F'+str(RowNo)].border=copy(DefaultCell.border)
                ws['F'+str(RowNo)].font=copy(DefaultCell.font)
                ws['J'+str(RowNo)]="=SUM(H{0}:I{0})".format(str(RowNo))
                ws['J'+str(RowNo)].border=copy(DefaultCell.border)
                ws['J'+str(RowNo)].font=copy(DefaultCell.font)
                ws['N'+str(RowNo)]="=SUM(L{0}:M{0})".format(str(RowNo))
                ws['N'+str(RowNo)].border=copy(DefaultCell.border)
                ws['N'+str(RowNo)].font=copy(DefaultCell.font)

                RowNo=RowNo+1
            ws.merge_cells('A{0}:A{1}'.format(str(RowNo-FeeItemDataCount),str(RowNo-1)))
            for num in range(RowNo-FeeItemDataCount,RowNo):
                ws['A'+str(num)].border=copy(DefaultCell.border)

            SubTotal.append(RowNo)
            ws['A'+str(RowNo)]='小計'
            ws['A'+str(RowNo)].border=copy(DefaultCell.border)
            ws['A'+str(RowNo)].font=copy(DefaultCell.font)
            ws['B'+str(RowNo)].border=copy(DefaultCell.border)
            ws['B'+str(RowNo)].font=copy(DefaultCell.font)
            ws['C'+str(RowNo)].border=copy(DefaultCell.border)
            ws['C'+str(RowNo)].font=copy(DefaultCell.font)
            #小計資料
            ws['D'+str(RowNo)]='=SUM(D{0}:D{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['D'+str(RowNo)].border=copy(DefaultCell.border)
            ws['D'+str(RowNo)].font=copy(DefaultCell.font)
            ws['E'+str(RowNo)]='=SUM(E{0}:E{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['E'+str(RowNo)].border=copy(DefaultCell.border)
            ws['E'+str(RowNo)].font=copy(DefaultCell.font)
            ws['F'+str(RowNo)]='=SUM(F{0}:F{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['F'+str(RowNo)].border=copy(DefaultCell.border)
            ws['F'+str(RowNo)].font=copy(DefaultCell.font)
            ws['G'+str(RowNo)]='=SUM(G{0}:G{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['G'+str(RowNo)].border=copy(DefaultCell.border)
            ws['G'+str(RowNo)].font=copy(DefaultCell.font)
            ws['H'+str(RowNo)]='=SUM(H{0}:H{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['H'+str(RowNo)].border=copy(DefaultCell.border)
            ws['H'+str(RowNo)].font=copy(DefaultCell.font)
            ws['I'+str(RowNo)]='=SUM(I{0}:I{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['I'+str(RowNo)].border=copy(DefaultCell.border)
            ws['I'+str(RowNo)].font=copy(DefaultCell.font)
            ws['J'+str(RowNo)]='=SUM(J{0}:J{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['J'+str(RowNo)].border=copy(DefaultCell.border)
            ws['J'+str(RowNo)].font=copy(DefaultCell.font)
            ws['K'+str(RowNo)]='=SUM(K{0}:K{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['K'+str(RowNo)].border=copy(DefaultCell.border)
            ws['K'+str(RowNo)].font=copy(DefaultCell.font)
            ws['L'+str(RowNo)]='=SUM(L{0}:L{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['L'+str(RowNo)].border=copy(DefaultCell.border)
            ws['L'+str(RowNo)].font=copy(DefaultCell.font)
            ws['M'+str(RowNo)]='=SUM(M{0}:M{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['M'+str(RowNo)].border=copy(DefaultCell.border)
            ws['M'+str(RowNo)].font=copy(DefaultCell.font)
            ws['N'+str(RowNo)]='=SUM(N{0}:N{1})'.format(str(RowNo-FeeItemDataCount),str(RowNo-1))
            ws['N'+str(RowNo)].border=copy(DefaultCell.border)
            ws['N'+str(RowNo)].font=copy(DefaultCell.font)

            RowNo=RowNo+1

    ws['A'+str(RowNo)]='總計'
    ws['A'+str(RowNo)].border=copy(DefaultCell.border)
    ws['A'+str(RowNo)].font=copy(DefaultCell.font)
    #總計資料
    ws['B'+str(RowNo)].border=copy(DefaultCell.border)
    ws['B'+str(RowNo)].font=copy(DefaultCell.font)
    ws['C'+str(RowNo)].border=copy(DefaultCell.border)
    ws['C'+str(RowNo)].font=copy(DefaultCell.font)
    SumCellStr=""
    for i in SubTotal:
        SumCellStr=SumCellStr+'{0}'+str(i)+','
    SumCellStr='=SUM('+SumCellStr[:len(SumCellStr)-1]+')'
    ws['D'+str(RowNo)]=SumCellStr.format('D')
    ws['D'+str(RowNo)].border=copy(DefaultCell.border)
    ws['D'+str(RowNo)].font=copy(DefaultCell.font)
    ws['E'+str(RowNo)]=SumCellStr.format('E')
    ws['E'+str(RowNo)].border=copy(DefaultCell.border)
    ws['E'+str(RowNo)].font=copy(DefaultCell.font)
    ws['F'+str(RowNo)]=SumCellStr.format('F')
    ws['F'+str(RowNo)].border=copy(DefaultCell.border)
    ws['F'+str(RowNo)].font=copy(DefaultCell.font)
    ws['G'+str(RowNo)]=SumCellStr.format('G')
    ws['G'+str(RowNo)].border=copy(DefaultCell.border)
    ws['G'+str(RowNo)].font=copy(DefaultCell.font)
    ws['H'+str(RowNo)]=SumCellStr.format('H')
    ws['H'+str(RowNo)].border=copy(DefaultCell.border)
    ws['H'+str(RowNo)].font=copy(DefaultCell.font)
    ws['I'+str(RowNo)]=SumCellStr.format('I')
    ws['I'+str(RowNo)].border=copy(DefaultCell.border)
    ws['I'+str(RowNo)].font=copy(DefaultCell.font)
    ws['J'+str(RowNo)]=SumCellStr.format('J')
    ws['J'+str(RowNo)].border=copy(DefaultCell.border)
    ws['J'+str(RowNo)].font=copy(DefaultCell.font)
    ws['K'+str(RowNo)]=SumCellStr.format('K')
    ws['K'+str(RowNo)].border=copy(DefaultCell.border)
    ws['K'+str(RowNo)].font=copy(DefaultCell.font)
    ws['L'+str(RowNo)]=SumCellStr.format('L')
    ws['L'+str(RowNo)].border=copy(DefaultCell.border)
    ws['L'+str(RowNo)].font=copy(DefaultCell.font)
    ws['M'+str(RowNo)]=SumCellStr.format('M')
    ws['M'+str(RowNo)].border=copy(DefaultCell.border)
    ws['M'+str(RowNo)].font=copy(DefaultCell.font)
    ws['N'+str(RowNo)]=SumCellStr.format('N')
    ws['N'+str(RowNo)].border=copy(DefaultCell.border)
    ws['N'+str(RowNo)].font=copy(DefaultCell.font)

    RowNo=RowNo+1
    ws['A'+str(RowNo)]='製表人'
    ws['C'+str(RowNo)]='出納'
    ws['F'+str(RowNo)]='業務主管'
    ws['I'+str(RowNo)]='主辦會計'
    ws['L'+str(RowNo)]='機關首長'

    return ws



def SetFeeItemReportExcel(StartDate,EndDate,ws):

    DealData=M_V_FeeItemReport.objects.filter(DealDate__range=(datetime.datetime.strptime(StartDate,'%Y-%m-%d'),datetime.datetime.strptime(EndDate,'%Y-%m-%d'))).values()
    if(len(DealData)==0):
        return None
    dt=datetime.datetime.now()
    ws['J4'] = '列印日期:{0}年{1}月{2}日'.format(dt.year-1911,dt.month,dt.day)
    ws['B5'] = datetime.datetime.strptime(StartDate,'%Y-%m-%d')
    ws['D5'] =datetime.datetime.strptime(EndDate,'%Y-%m-%d')
    i=9

    for value in DealData:
        ws['A'+str(i)] = value['StationID']
        ws['B'+str(i)] = value['DealDate'].date()
        ws['C'+str(i)] = value['DealDate'].time()
        ws['D'+str(i)] = '作廢' if value['Status']=='0' else '正常'
        ws['E'+str(i)] = value['FeeID']
        ws['F'+str(i)] = value['FeeName']
        ws['G'+str(i)] = value['Qty']
        ws['H'+str(i)] = value['Amount']
        ws['I'+str(i)] = value['Amount'] if value['PayType']=='PT01' else 0
        ws['J'+str(i)] = value['Amount'] if value['PayType']=='PT02' else 0
        ws['K'+str(i)] = value['InvoiceNo']
        ws['L'+str(i)] = value['Remark']
        i=i+1
    ws['A'+str(i)] = '筆數'
    ws['B'+str(i)] = len(DealData)
    ws['C'+str(i)] = '數量總計'
    ws['D'+str(i)] = DealData.aggregate(Sum('Qty'))['Qty__sum']
    ws['E'+str(i)] = '金額合計(不含作廢):'
    ws['F'+str(i)] = DealData.filter(Status='1').aggregate(Sum('Amount'))['Amount__sum']
    ws['G'+str(i)] = '金額合計(作廢):'
    ws['H'+str(i)] = DealData.filter(Status='0').aggregate(Sum('Amount'))['Amount__sum']
    i=i+2
    ws['A'+str(i)] = '機關主管：'
    ws['D'+str(i)] = '主辦會計：'
    ws['H'+str(i)] = '出　　納：'
    ws['K'+str(i)] = '業務主管：'
    ws['N'+str(i)] = '製　　表：'


    return ws



def SetPenaltyReportExcel(StartDate,EndDate,ws):
    DealData=M_V_PenaltyReport.objects.filter(DealDate__range=(datetime.datetime.strptime(StartDate,'%Y-%m-%d'),datetime.datetime.strptime(EndDate,'%Y-%m-%d'))).values()
    if(len(DealData)==0):
        return None
    dt=datetime.datetime.now()
    ws['F4'] = '列印日期:{0}年{1}月{2}日'.format(dt.year-1911,dt.month,dt.day)
    ws['C6'] = datetime.datetime.strptime(StartDate,'%Y-%m-%d')
    ws['F6'] =datetime.datetime.strptime(EndDate,'%Y-%m-%d')
    i=10

    for value in DealData:
        ws['A'+str(i)] = value['DealDate'].date()
        ws['B'+str(i)] = value['PenaltyID']
        ws['C'+str(i)] = value['PenaltyName']
        ws['D'+str(i)] = value['TermID']
        ws['E'+str(i)] = value['TermName']
        ws['G'+str(i)] = value['qty']
        ws['H'+str(i)] = value['totalamount']
        ws['I'+str(i)] = value['Remark']
        i=i+1
    ws['A'+str(i)] = '筆數'
    ws['B'+str(i)] = len(DealData)
    ws['C'+str(i)] = '數量總計'
    ws['D'+str(i)] = DealData.aggregate(Sum('qty'))['qty__sum']
    ws['E'+str(i)] = '金額合計:'
    ws['F'+str(i)] = DealData.aggregate(Sum('totalamount'))['totalamount__sum']
    i=i+2
    ws['A'+str(i)] = '機關主管：'
    ws['C'+str(i)] = '主辦會計：'
    ws['E'+str(i)] = '出　　納：'
    ws['G'+str(i)] = '業務主管：'
    ws['I'+str(i)] = '製　　表：'
    return ws

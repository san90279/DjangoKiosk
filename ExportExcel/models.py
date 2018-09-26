from django.db import models
from Deal.models import M_DealMaster

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

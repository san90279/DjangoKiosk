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

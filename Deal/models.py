from django.db import models

# Create your models here.
class M_DealMaster(models.Model):

    DealStatusList=(
        ('0','作廢'),
    )
    PayTypeList=(
        ('PT01','現金'),
        ('PT02','悠遊卡'),
    )


    StationID=models.ForeignKey('Station.M_Station',on_delete=models.PROTECT)
    DealDate=models.DateTimeField()
    Status=models.CharField(max_length=10,choices=DealStatusList,null=True)
    Cashier=models.ForeignKey('EmployeeCard.M_EmployeeCard',on_delete=models.PROTECT)
    Amount=models.IntegerField(default=0)
    PayType=models.CharField(max_length=10,choices=PayTypeList)
    InvoiceNo=models.ForeignKey('Invoice.M_Invoice',on_delete=models.PROTECT)
    IsCheckout=models.BooleanField()
    IsOutside=models.BooleanField()
    Creator=models.ForeignKey('auth.user',on_delete=models.PROTECT,related_name='CreatorMaster')
    CreateDate=models.DateTimeField(auto_now=True)
    Editor=models.ForeignKey('auth.user',on_delete=models.PROTECT,null=True,related_name='EditorMaster')
    EditDate=models.DateTimeField(auto_now=True,null=True)


class M_DealDetail(models.Model):
    MasterID=models.ForeignKey('Deal.M_DealMaster',on_delete=models.PROTECT)
    FeeID=models.ForeignKey('FeeItem.M_FeeItem',on_delete=models.PROTECT)
    Amount=models.IntegerField(default=0)
    Qty=models.IntegerField(default=0)
    TotalAmount=models.IntegerField(default=0)
    Remark=models.CharField(max_length=100,null=True)
    Creator=models.ForeignKey('auth.user',on_delete=models.PROTECT,related_name='CreatorDetail')
    CreateDate=models.DateTimeField(auto_now=True)
    Editor=models.ForeignKey('auth.user',on_delete=models.PROTECT,null=True,related_name='EditorDetail')
    EditDate=models.DateTimeField(auto_now=True,null=True)

from django.db import models
from FeeItem.models import M_FeeItem

# Create your models here.
class M_DealMaster(models.Model):

    DealStatusList=(
        ('0','作廢'),
        ('1','正常'),
    )
    PayTypeList=(
        ('PT01','現金'),
        ('PT02','悠遊卡'),
    )
    StationID=models.ForeignKey('Store.M_Station',on_delete=models.PROTECT)
    DealDate=models.DateTimeField()
    Status=models.CharField(max_length=10,choices=DealStatusList,null=True)
    Cashier=models.ForeignKey('auth.user',on_delete=models.PROTECT)
    Amount=models.IntegerField(default=0)
    PayType=models.CharField(max_length=10,choices=PayTypeList)
    InvoiceNo=models.ForeignKey('Invoice.M_Invoice',on_delete=models.PROTECT)
    IsCheckout=models.BooleanField()
    IsOutside=models.BooleanField()
    LotNo=models.IntegerField(default=1)
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
    PenaltyID=models.ForeignKey('Penalty.M_Penalty',on_delete=models.PROTECT,null=True)
    TermID=models.ForeignKey('Term.M_Term',on_delete=models.PROTECT,null=True)
    Creator=models.ForeignKey('auth.user',on_delete=models.PROTECT,related_name='CreatorDetail')
    CreateDate=models.DateTimeField(auto_now=True)
    Editor=models.ForeignKey('auth.user',on_delete=models.PROTECT,null=True,related_name='EditorDetail')
    EditDate=models.DateTimeField(auto_now=True,null=True)
#交易補登DB VIEW MODEL
class M_V_entry(models.Model):
    id = models.BigIntegerField(primary_key=True)
    DealDate=models.DateTimeField()
    username=models.CharField(max_length=10,unique=True)
    last_name=models.CharField(max_length=50)
    StationID=models.CharField(max_length=10,unique=True)
    FeeID=models.CharField(max_length=10,unique=True)
    FeeName=models.CharField(max_length=50)
    beginno=models.CharField(max_length=20,unique=True)
    PayType=models.CharField(max_length=10,choices=M_DealMaster.PayTypeList)
    Amount=models.IntegerField(default=0)
    Qty=models.IntegerField(default=0)
    TotalAmount=models.IntegerField(default=0)
    Status=models.CharField(max_length=10,choices=M_DealMaster.DealStatusList,null=True)
    IsCheckout=models.BooleanField()
    LotNo=models.IntegerField(default=1)
    class Meta:
        managed = False
        db_table = "Deal_M_V_entry"

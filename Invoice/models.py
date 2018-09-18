from django.db import models

# Create your models here.
class M_Invoice(models.Model):

    InvoiceStatusList=(
        ('0','作廢'),
        ('1','已使用'),
        ('2','未使用'),
    )

    FeeID=models.ForeignKey('FeeItem.M_FeeItem',on_delete=models.PROTECT)
    InvoiceNo=models.CharField(max_length=20,unique=True)
    Status=models.CharField(max_length=10,choices=InvoiceStatusList)
    Amount=models.IntegerField(null=True)
    StationID=models.ForeignKey('Store.M_Station',on_delete=models.PROTECT)
    LotNo=models.IntegerField()
    Creator=models.ForeignKey('auth.user',on_delete=models.PROTECT,related_name='Creator')
    CreateDate=models.DateTimeField(auto_now=True)
    Editor=models.ForeignKey('auth.user',on_delete=models.PROTECT,null=True,related_name='Editor')
    EditDate=models.DateTimeField(null=True)


class M_V_Invoice(models.Model):
    MaxInvoice=models.CharField(max_length=20)
    MinInvoice=models.CharField(max_length=20)
    TotalInvoice=models.IntegerField()
    TotalAmount=models.IntegerField()
    Status=models.CharField(max_length=10,choices=M_Invoice.InvoiceStatusList)
    StationID=models.CharField(max_length=10)
    StationName=models.CharField(max_length=50)
    FeeID=models.CharField(max_length=10)
    FeeName=models.CharField(max_length=50)
    LotNo=models.IntegerField()
    class Meta:
        managed = False
        db_table = "Invoice_M_V_Invoice"

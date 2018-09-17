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
    Creator=models.ForeignKey('auth.user',on_delete=models.PROTECT,related_name='Creator')
    CreateDate=models.DateTimeField(auto_now=True)
    Editor=models.ForeignKey('auth.user',on_delete=models.PROTECT,null=True,related_name='Editor')
    EditDate=models.DateTimeField(null=True)


class M_V_Invoice(models.Model):
    InvoiceNo=models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = "Invoice_M_V_Invoice"

from django.db import models

# Create your models here.
class M_Checkout(models.Model):

    RecordTime=models.DateTimeField(null=True)
    CloseDate=models.DateField()
    Editor=models.ForeignKey('auth.user',on_delete=models.PROTECT,null=True)

from django.db import models

# Create your models here.
class M_PrintData(models.Model):
    EnableDate=models.DateTimeField()
    Salesman=models.CharField(max_length=50)
    Accounting=models.CharField(max_length=50)
    Chief=models.CharField(max_length=50)
    Tel=models.CharField(max_length=50)
    Fax=models.CharField(max_length=50)
    Editor=models.ForeignKey('auth.user',on_delete=models.PROTECT)
    EditDate=models.DateTimeField(auto_now=True)

from django.db import models

# Create your models here.
class M_Store(models.Model):

    StoreID=models.CharField(max_length=10,unique=True)
    StoreName=models.CharField(max_length=50)
    Editor=models.ForeignKey('auth.user',on_delete=models.PROTECT)
    EditDate=models.DateTimeField(auto_now=True)

class M_Station(models.Model):

    StoreID=models.ForeignKey('M_Store',on_delete=models.PROTECT)
    StationID=models.CharField(max_length=10,unique=True)
    StationName=models.CharField(max_length=50)
    Editor=models.ForeignKey('auth.user',on_delete=models.PROTECT)
    EditDate=models.DateTimeField(auto_now=True)

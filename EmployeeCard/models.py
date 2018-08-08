from django.db import models

# Create your models here.
class M_EmployeeCard(models.Model):

    EmployeeID=models.CharField(max_length=10,unique=True)
    EmployeeName=models.CharField(max_length=20)
    CardNo=models.CharField(max_length=50,unique=True)
    IsWork=models.BooleanField(default=True)
    Editor=models.ForeignKey('auth.user',on_delete=models.PROTECT)
    EditDate=models.DateTimeField(auto_now=True)

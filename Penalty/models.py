from django.db import models

class M_Penalty(models.Model):

    PenaltyID=models.CharField(max_length=20,unique=True)
    PenaltyName=models.CharField(max_length=50)
    Remark=models.CharField(max_length=100,null=True)
    Editor=models.ForeignKey('auth.user',on_delete=models.PROTECT)
    EditDate=models.DateTimeField(auto_now=True)

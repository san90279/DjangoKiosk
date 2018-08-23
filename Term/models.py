from django.db import models

# Create your models here.
class M_Term(models.Model):
    TermID=models.CharField(max_length=10,unique=True)
    TermName=models.CharField(max_length=50)
    Remark=models.CharField(max_length=100,null=True)
    Editor=models.ForeignKey('auth.user',on_delete=models.PROTECT)
    EditDate=models.DateTimeField(auto_now=True)

from django.db import models

# Create your models here.
class M_FeeItem(models.Model):

    FeeStatusList=(
        ('0','停用'),
        ('1','啟用'),
    )
    FeeTypeList=(
        ('FY01','資料使用費'),
        ('FY04','登記費'),
        ('FY03','證照費'),
        ('FY02','服務費'),
        ('FY05','規費'),
        ('FY06','罰緩'),
        ('FY07','考試報名費'),
        ('FY08','其他'),
    )

    FeeID=models.CharField(max_length=10,unique=True)
    FeeName=models.CharField(max_length=50)
    FeeAmount=models.IntegerField(default=0)
    Remark=models.CharField(max_length=100,null=True)
    FeeType=models.CharField(max_length=10,choices=FeeTypeList)
    Status=models.CharField(max_length=10,choices=FeeStatusList)
    OrderBy=models.IntegerField(default=99)
    Editor=models.ForeignKey('auth.user',on_delete=models.PROTECT)
    EditDate=models.DateTimeField(auto_now=True)

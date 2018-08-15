from django.db import models

# Create your models here.
class M_Menu(models.Model):
    MenuTypeList=(
        ('MT01','功能選項'),#有子項
        ('MT02','連結選項'),#沒有子項
    )


    MenuName=models.CharField(max_length=100)
    MenuLink=models.CharField(max_length=100,null=True)
    MenuType=models.CharField(max_length=10,choices=MenuTypeList)
    MenuParent=models.BigIntegerField(null=True)
    MenuIcon=models.CharField(max_length=50,default='')
    IsActive=models.BooleanField()

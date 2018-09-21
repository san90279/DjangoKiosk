from django import forms
from Store.models import M_Station
from FeeItem.models import M_FeeItem
from Deal.models import M_DealMaster
from Invoice.models import M_Invoice
from EmployeeCard.models import M_EmployeeCard

class EntryForm(forms.Form):
    DealDate=forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','type':'Date'}),label='補登日期')
    beginno=forms.CharField(max_length=20,label='起始號碼',widget=forms.TextInput(attrs={'class': 'form-control'}))
    PayType=forms.CharField(max_length=10,label='收款別')
    StationID=forms.CharField(label='站點')
    FeeID=forms.CharField(label='規費')
    EmployeeCardID=forms.CharField(label='收銀人員')
    Qty=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),label='張數')


    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['StationID'].widget=forms.Select(attrs={'class':'form-control'},choices= M_Station.objects.all().values_list('id', 'StationName'))
        self.fields['FeeID'].widget=forms.Select(attrs={'class':'form-control'},choices= M_FeeItem.objects.all().values_list('id', 'FeeName'))
        self.fields['EmployeeCardID'].widget=forms.Select(attrs={'class':'form-control'},choices= M_EmployeeCard.objects.all().values_list('id', 'EmployeeName'))
        self.fields['PayType'].widget=forms.Select(attrs={'class':'form-control'},choices= M_DealMaster.PayTypeList)

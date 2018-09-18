from django import forms
from Store.models import M_Station
from FeeItem.models import M_FeeItem



class AddInvoiceForm(forms.Form):

    StartInvoiceNo=forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class': 'form-control'}),label='起始序號')
    StationID=forms.CharField(label='站點')
    FeeID=forms.CharField(label='規費')
    AddCount=forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='張數')
    def __init__(self, *args, **kwargs):
        super(AddInvoiceForm, self).__init__(*args, **kwargs)
        self.fields['StationID'].widget=forms.Select(attrs={'class':'form-control'},choices= M_Station.objects.all().values_list('id', 'StationName'))
        self.fields['FeeID'].widget=forms.Select(attrs={'class':'form-control'},choices= M_FeeItem.objects.all().values_list('id', 'FeeName'))

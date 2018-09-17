from django import forms
from Store.models import M_Station,M_Store

class StationForm(forms.ModelForm):
    class Meta():
        model=M_Station
        fields=['StoreID','StationID','StationName']
    def __init__(self,*args, **kwargs):
        super(StationForm, self).__init__(*args, **kwargs)
        self.fields['StoreID'].widget=forms.Select(attrs={'class':'form-control'},choices= M_Store.objects.all().values_list('id', 'StoreName'))
        self.fields['StationID'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['StationName'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['StoreID'].label='戶所名稱'
        self.fields['StationID'].label='站點代碼'
        self.fields['StationName'].label='站點名稱'

class StoreForm(forms.ModelForm):
    class Meta():
        model=M_Store
        fields=['StoreID','StoreName']
    def __init__(self,*args, **kwargs):
        super(StoreForm, self).__init__(*args, **kwargs)
        self.fields['StoreID'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['StoreName'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['StoreID'].label='戶所代碼'
        self.fields['StoreName'].label='戶所名稱'

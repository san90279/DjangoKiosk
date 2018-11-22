from django import forms
from FeeItem.models import M_FeeItem

class FeeItemForm(forms.ModelForm):
    class Meta():
        model=M_FeeItem
        fields=['FeeID','FeeName','FeeAmount','Remark','FeeType','Status','OrderBy']
    def __init__(self,*args, **kwargs):
        super(FeeItemForm, self).__init__(*args, **kwargs)
        self.fields['FeeID'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['FeeName'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['FeeAmount'].widget=forms.NumberInput(attrs={'class':'form-control'})
        self.fields['FeeType'].widget=forms.Select(attrs={'class':'form-control'},choices=M_FeeItem.FeeTypeList)
        self.fields['OrderBy'].widget=forms.NumberInput(attrs={'class':'form-control'})
        self.fields['Status'].widget=forms.Select(attrs={'class':'form-control'},choices=M_FeeItem.FeeStatusList)
        self.fields['Status'].initial = 1
        self.fields['Remark'].widget=forms.Textarea(attrs={'class':'form-control'})
        self.fields['FeeID'].label='規費項目代碼'
        self.fields['FeeName'].label='規費項目名稱'
        self.fields['FeeAmount'].label='規費金額'
        self.fields['Remark'].label='項目描述'
        self.fields['FeeType'].label='規費群組'
        self.fields['Status'].label='狀態'
        self.fields['OrderBy'].label='排序'

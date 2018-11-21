from django import forms
from PrintData.models import M_PrintData

class PrintDataForm(forms.ModelForm):
    class Meta():
        model=M_PrintData
        fields=['EnableDate','Salesman','Accounting','Chief','Tel','Fax']
    def __init__(self,*args, **kwargs):
        super(PrintDataForm, self).__init__(*args, **kwargs)
        self.fields['EnableDate'].widget=forms.TextInput(attrs={'class':'form-control','type':'Date'})
        self.fields['Salesman'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['Accounting'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['Chief'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['Tel'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['Fax'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['EnableDate'].label='啟用日期'
        self.fields['Salesman'].label='業務課長'
        self.fields['Accounting'].label='主辦會計'
        self.fields['Chief'].label='機關主管'
        self.fields['Tel'].label='電話'
        self.fields['Fax'].label='傳真'

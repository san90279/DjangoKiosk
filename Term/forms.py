from django import forms
from .models import M_Term

class TermForm(forms.ModelForm):
    class Meta():
        model=M_Term
        fields=['TermID','TermName','Remark']

    #def TermForm(self):

    def __init__(self,*args, **kwargs):
        super(TermForm, self).__init__(*args, **kwargs)
        self.fields['TermID'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['TermName'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['Remark'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['TermID'].label='條款編號'
        self.fields['TermName'].label='條款名稱'
        self.fields['Remark'].label='備註'

from django import forms
from Penalty.models import M_Penalty

class PenaltyForm(forms.ModelForm):
    class Meta():
        model=M_Penalty
        fields=['PenaltyID','PenaltyName','Remark']
    def __init__(self,*args, **kwargs):
        super(PenaltyForm, self).__init__(*args, **kwargs)
        self.fields['PenaltyID'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['PenaltyName'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['Remark'].widget=forms.Textarea(attrs={'class':'form-control'})
        self.fields['PenaltyID'].label='罰緩編號'
        self.fields['PenaltyName'].label='罰緩名稱'
        self.fields['Remark'].label='備註'

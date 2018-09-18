from django import forms
from Checkout.models import M_Checkout

class CheckoutForm(forms.ModelForm):
    class Meta():
        model=M_Checkout
        fields=['CloseDate',]
    def __init__(self,*args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['CloseDate'].widget=forms.TextInput(attrs={'type':'date'})
        self.fields['CloseDate'].label='過帳日期'

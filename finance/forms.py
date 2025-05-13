from django import forms
from .models import Bank , BankAccount

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = '__all__' 
        
class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['bank','account_name','account_type','account_number'] 
        
        
        
        
  
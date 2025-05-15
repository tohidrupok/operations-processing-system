from django import forms
from .models import Bank , BankAccount, Transaction
from core.models import Project

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = '__all__' 
        
class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['bank','account_name','account_type','account_number'] 
        
        
    
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['project','amount','type','bank','voucher_no','voucher_date','company_account'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(status='RUNNING')
        
  
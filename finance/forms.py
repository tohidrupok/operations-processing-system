from django import forms
from .models import Bank , BankAccount, Transaction, SupplierPayment, MenPowerPayment
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
        
  
class SupplierPaymentForm(forms.ModelForm):
    class Meta:
        model = SupplierPayment
        fields = ['memo', 'amount', 'type', 'bank_account', 'check_number', 'is_payment_done']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'check_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'If not Cash'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_payment_done': forms.CheckboxInput(),
        }
        
        
class MenPowerPaymentForm(forms.ModelForm):
    class Meta:
        model = MenPowerPayment
        fields = ['menpowermemo', 'amount', 'type', 'bank_account', 'check_number', 'is_payment_done']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'check_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'If not Cash'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_payment_done': forms.CheckboxInput(),
        }
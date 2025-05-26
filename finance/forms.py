from django import forms
from .models import Bank , BankAccount, Transaction, SupplierPayment, MenPowerPayment, Loan, PayLoan
from core.models import Project, Memo, ManpowerMemo

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
        fields = ['project','amount','type','bank','cheque_number' ,'cheque_date', 'voucher_no','voucher_date','company_account'] 
        widgets = {
            'cheque_date': forms.DateInput(attrs={'type': 'date'}),
            'voucher_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
        
    def clean(self):
        cleaned_data = super().clean()
        client_payment_type = cleaned_data.get('type')
    

        if client_payment_type == 'CHEQUE':
            if not cleaned_data.get('cheque_number'):
                self.add_error('cheque_number', 'This field is required for cheque loans.')
            if not cleaned_data.get('cheque_date'):
                self.add_error('cheque_date', 'This field is required for cheque loans.')
            if not cleaned_data.get('voucher_no'):
                self.add_error('voucher_no', 'This field is required for cheque loans.')
            if not cleaned_data.get('voucher_date'):
                self.add_error('voucher_date', 'This field is required for cheque loans.')
            if not cleaned_data.get('bank'):
                self.add_error('bank', 'This field is required for cheque loans.')
        return cleaned_data 
        
  
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
        
    def __init__(self, *args, **kwargs):
        super(SupplierPaymentForm, self).__init__(*args, **kwargs)
        # Filter memo options: only those not fully paid
        self.fields['memo'].queryset = Memo.objects.filter(is_payment_done=False)
        self.fields['memo'].widget.attrs.update({'class': 'form-control'})
        self.fields['bank_account'].widget.attrs.update({'class': 'form-control'})
        
        
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
        
    def __init__(self, *args, **kwargs):
        super(MenPowerPaymentForm, self).__init__(*args, **kwargs)
        self.fields['menpowermemo'].queryset = ManpowerMemo.objects.filter(is_payment_done=False)
        self.fields['menpowermemo'].widget.attrs.update({'class': 'form-control'})
        self.fields['bank_account'].widget.attrs.update({'class': 'form-control'})  
        
        
        
class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'
        widgets = {
            'cheque_date': forms.DateInput(attrs={'type': 'date'}),
            'voucher_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        loan_giver_type = kwargs.pop('loan_giver_type', None)
        super().__init__(*args, **kwargs)

        if loan_giver_type in ['CASH', 'BANK', 'MOBILE', 'CHEQUE']:
            self.fields['bank_account'].queryset = BankAccount.objects.filter(account_type=loan_giver_type)
        else:
            self.fields['bank_account'].queryset = BankAccount.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        loan_type = cleaned_data.get('loan_giver_type')
        bank_account = cleaned_data.get('bank_account')
        
        if not bank_account:
           raise forms.ValidationError("Bank account is required when loan giver type is BANK.")

        if loan_type == 'CHEQUE':
            if not cleaned_data.get('cheque_number'):
                self.add_error('cheque_number', 'This field is required for cheque loans.')
            if not cleaned_data.get('cheque_date'):
                self.add_error('cheque_date', 'This field is required for cheque loans.')
            if not cleaned_data.get('voucher_number'):
                self.add_error('voucher_number', 'This field is required for cheque loans.')
            if not cleaned_data.get('voucher_date'):
                self.add_error('voucher_date', 'This field is required for cheque loans.')
        return cleaned_data 
    
    
class PayLoanForm(forms.ModelForm):
    class Meta:
        model = PayLoan
        fields = ['amount', 'payloan_giver_type', 'bank_account', 'cheque_number', 'cheque_date', 'note']
        
        widgets = {
            'cheque_date': forms.DateInput(attrs={'type': 'date'}),
            
        }
     
        
    def clean(self):
        cleaned_data = super().clean()
        loan_type = cleaned_data.get('payloan_giver_type')

        if loan_type == 'CHEQUE':
            if not cleaned_data.get('cheque_number'):
                self.add_error('cheque_number', 'This field is required for cheque loans.')
            if not cleaned_data.get('cheque_date'):
                self.add_error('cheque_date', 'This field is required for cheque loans.')
        return cleaned_data
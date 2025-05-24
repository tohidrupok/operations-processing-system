from django.db import models
from core.models import Project

# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name  


# BankAccount Model
class BankAccount(models.Model):
    ACCOUNT_TYPES = [
        ('CASH', 'Cash'),
        ('BANK', 'Bank Deposit'),
        ('MOBILE', 'Bkash / Nogod / Rocket'),
        ('CHEQUE', 'Cheque'),
    ]

    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True, help_text="Select bank name")
    account_name = models.CharField(max_length=100, help_text="Account holder's name")
    account_number = models.CharField(max_length=50, unique=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='SAVINGS')
    balance = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_name}, {self.bank}"

    def credit(self, amount):
        """Increase balance"""
        if amount > 0:
            self.balance += amount
            self.save()
            return True
        return False

    def debit(self, amount):
        """Decrease balance if enough money exists"""
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.save()
            return True
        return False

    class Meta:
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"



class Transaction(models.Model):
    TYPE_CHOICES = [
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
        ('FTGS', 'FTGS'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('CANCELLED', 'Cancelled'),
    ]

    project = models.ForeignKey('core.Project', on_delete=models.CASCADE, related_name='transactions')
    amount = models.PositiveIntegerField(help_text="Maximum allowed is 10,000,000 TK")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    bank = models.ForeignKey('Bank', on_delete=models.SET_NULL, null=True, blank=True, help_text="Only fill this if payment is not Cash.")
    voucher_no = models.CharField(max_length=100, null=True, blank=True,  help_text="Only fill this if payment is not Cash.")
    voucher_date = models.DateField(null=True, blank=True, help_text="Example: 2025-12-31")
    receive_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    company_account = models.ForeignKey('BankAccount', on_delete=models.PROTECT) 
    
    created_at = models.DateTimeField(auto_now_add=True, help_text="Transaction creation timestamp")
    updated_at = models.DateTimeField(auto_now=True, help_text="Transaction last updated")

    def __str__(self):
        return f"{self.project} - {self.amount} - {self.get_type_display()}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-voucher_date']
 
 
class SupplierPayment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
        ('FTGS', 'FTGS'),
        ('OTHER', 'Other'),
    ]

    memo = models.ForeignKey('core.Memo', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    bank_account = models.ForeignKey('BankAccount', on_delete=models.PROTECT)
    check_number = models.CharField(max_length=100, blank=True, null=True, help_text="Only fill this if payment is not Cash.")
    is_payment_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"SupplierPayment: {self.memo} - {self.amount} ({self.type})"
    
    
class MenPowerPayment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
        ('FTGS', 'FTGS'),
        ('OTHER', 'Other'),
    ]

    menpowermemo = models.ForeignKey('core.ManpowerMemo', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    bank_account = models.ForeignKey('BankAccount', on_delete=models.PROTECT)
    check_number = models.CharField(max_length=100, blank=True, null=True, help_text="Only fill this if payment is not Cash.")
    is_payment_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"MenPowerPayment: {self.menpowermemo} - {self.amount} ({self.type})"
    
    
    

class Loan(models.Model):
    LOAN_GIVER_TYPE_CHOICES = [
        ('CASH', 'Cash'),
        ('BANK', 'Bank Deposit'),
        ('MOBILE', 'Bkash / Nogod / Rocket'),
        ('CHEQUE', 'Cheque'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Loan Approved'),
        ('PAID', 'Payment Done'),
        
    ]

    loan_provider_name = models.CharField(max_length=100, help_text="Name of the person or organization giving the loan")
    loan_giver_type = models.CharField(max_length=10, choices=LOAN_GIVER_TYPE_CHOICES)
    amount = models.PositiveIntegerField()
    bank_account = models.ForeignKey('BankAccount', on_delete=models.SET_NULL, null=True, blank=True, help_text="Linked bank account if applicable")
    payment_amount = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    cheque_number = models.CharField(max_length=50, blank=True, null=True)
    cheque_date = models.DateField(blank=True, null=True)

    voucher_number = models.CharField(max_length=50, blank=True, null=True)
    voucher_date = models.DateField(blank=True, null=True)
    receive_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.loan_provider_name} - {self.amount} ({self.get_status_display()})"
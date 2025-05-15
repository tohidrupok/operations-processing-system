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
        ('SAVINGS', 'Savings'),
        ('CURRENT', 'Current'),
        ('FIXED', 'Fixed Deposit'),
    ]

    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True, help_text="Select bank name")
    account_name = models.CharField(max_length=100, help_text="Account holder's name")
    account_number = models.CharField(max_length=50, unique=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='SAVINGS')
    balance = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bank.name} - {self.account_number}"

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
    amount = models.PositiveIntegerField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    bank = models.ForeignKey('Bank', on_delete=models.SET_NULL, null=True, blank=True)
    voucher_no = models.CharField(max_length=100, null=True, blank=True)
    voucher_date = models.DateField(null=True, blank=True)
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
 
 
 
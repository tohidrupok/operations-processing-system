from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import *
from .forms import * 
from django.contrib import messages
from django.utils import timezone
from django.db import transaction as db_transaction

def staff_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_staff)(view_func) 



# Bank List
@staff_required
def bank_list(request):
    banks = Bank.objects.all()
    return render(request, 'bank/bank_list.html', {'banks': banks})

# Create
@staff_required
def bank_create(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bank_list')
    else:
        form = BankForm()
    return render(request, 'bank/bank_form.html', {'form': form})



#Account list
# Bank List
@staff_required
def bank_accounts_list(request):
    accounts = BankAccount.objects.all()
    total_balance = sum(account.balance for account in accounts)
    total_accounts = accounts.count()
    return render(request, 'bank/bank_account_list.html', {
        'accounts': accounts,
        'total_balance': total_balance,
        'total_accounts': total_accounts
    })

# Create
@staff_required
def bank_accounts_create(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bank_account_list')
    else:
        form = BankAccountForm()
    return render(request, 'bank/bank_form.html', {'form': form})


# Update 
@staff_required
def bank_accounts_update(request, pk):
    account = get_object_or_404(BankAccount, pk=pk)
    if request.method == 'POST':
        form = BankAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('bank_account_list')
    else:
        form = BankAccountForm(instance=account)
    return render(request, 'bank/bank_form.html', {'form': form})




#List all transactions
@staff_required
def transaction_list(request):
    transactions = Transaction.objects.exclude(status='APPROVED')
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})


#Create new transaction
@staff_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/transaction_form.html', {'form': form})


#Update transaction
@staff_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/transaction_form.html', {'form': form})


#Delete transaction
@staff_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'transactions/transaction_confirm_delete.html', {'transaction': transaction})

#View transaction details
@staff_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'transactions/transaction_detail.html', {'transaction': transaction}) 







@staff_required
def transaction_approve(request, pk):
    transaction_obj = get_object_or_404(Transaction, pk=pk)

    if transaction_obj.status == 'APPROVED':
        messages.warning(request, "Transaction is already approved.")
        return redirect('transaction_detail', pk=pk)

    if request.method == 'POST':
        try:
            with db_transaction.atomic():
                # 1. Set receive_date = today
                transaction_obj.receive_date = timezone.now().date()

                # 2. Add payment to project (call model method)
                transaction_obj.project.add_payment(transaction_obj.amount)

                # 3. Credit company_account balance
                credited = transaction_obj.company_account.credit(transaction_obj.amount)
                if not credited:
                    raise ValueError("Failed to credit BankAccount balance.")

                # 4. Change status to APPROVED
                transaction_obj.status = 'APPROVED'
                transaction_obj.save()

            messages.success(request, "Transaction approved successfully.")
        except Exception as e:
            messages.error(request, f"Failed to approve transaction: {e}")

        return redirect('transaction_detail', pk=pk)

    # If GET or others - just redirect or show error
    messages.error(request, "Invalid request method.")
    return redirect('transaction_detail', pk=pk) 




@staff_required
def create_supplier_payment(request):
    if request.method == 'POST':
        form = SupplierPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier Payment created successfully.")
            return redirect('supplier_payment_list')
    else:
        form = SupplierPaymentForm()
    
    return render(request, 'payment/supplier_payment_form.html', {'form': form})  


@staff_required
def supplier_payment_list(request):
    payments = SupplierPayment.objects.select_related('memo', 'bank_account').all().order_by('-id')[:150]
    return render(request, 'payment/supplier_payment_list.html', {'payments': payments})


@staff_required
def create_menpower_payment(request):
    if request.method == 'POST':
        form = MenPowerPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier Payment created successfully.")
            return redirect('menpower_payment_list')
    else:
        form = MenPowerPaymentForm()
    
    return render(request, 'payment/menpower_payment_form.html', {'form': form})  


@staff_required
def menpower_payment_list(request):
    payments = MenPowerPayment.objects.select_related('menpowermemo', 'bank_account').all().order_by('-id')[:150]
    return render(request, 'payment/menpower_payment_list.html', {'payments': payments}) 


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import *
from .forms import * 

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


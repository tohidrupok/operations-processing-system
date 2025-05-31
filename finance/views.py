from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import *
from core.models import Company, Supplier
from .forms import * 
from django.contrib import messages
from django.utils import timezone
from django.db import transaction as db_transaction
from datetime import date, timedelta
from django.db.models import Sum, F, ExpressionWrapper, IntegerField, Value




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
from django.db import transaction



@staff_required
def create_supplier_payment(request):
    if request.method == 'POST':
        form = SupplierPaymentForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                payment = form.save(commit=False)
                bank_account = payment.bank_account

                
                if bank_account.balance < payment.amount:
                    messages.error(request, "❌ Not enough balance in the selected Bank Account.")
                    return render(request, 'payment/supplier_payment_form.html', {'form': form})

                bank_account.balance -= payment.amount
                bank_account.save()

            
                memo = payment.memo
                memo.payment_balance += payment.amount 
                
                #auto ispaymentstatus change  
                if  memo.payment_balance >= memo.amount:
                    memo.is_payment_done = True
                     
                # #manual ispaymentstatus change    
                # if payment.is_payment_done:
                #     memo.is_payment_done = True
                    
                memo.save()

                # Save payment
                payment.save()

            
            messages.success(request, "✅ Supplier Payment created successfully.")
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
            with transaction.atomic():
                payment = form.save(commit=False)

                # Step 1: Check bank balance before proceeding
                bank = payment.bank_account
                if bank.balance < payment.amount:
                    messages.error(request, "❌ Not enough balance in the selected Bank Account.")
                    return render(request, 'payment/menpower_payment_form.html', {'form': form})

                # Step 2: Deduct balance
                bank.balance -= payment.amount
                bank.save()

                # Step 3: Update ManpowerMemo
                memo = payment.menpowermemo
                memo.payment_balance += payment.amount
                
                #auto ispaymentstatus change  
                if  memo.payment_balance >= memo.amount:
                    memo.is_payment_done = True
                    
                # #manual ispaymentstatus change    
                # if payment.is_payment_done:
                #     memo.is_payment_done = True
                    
                memo.save()

                # Step 4: Save payment
                payment.save()

            messages.success(request, "✅ MenPower Payment created successfully.")
            return redirect('menpower_payment_list')
    else:
        form = MenPowerPaymentForm()
    
    return render(request, 'payment/menpower_payment_form.html', {'form': form}) 


@staff_required
def menpower_payment_list(request):
    payments = MenPowerPayment.objects.select_related('menpowermemo', 'bank_account').all().order_by('-id')[:150]
    return render(request, 'payment/menpower_payment_list.html', {'payments': payments}) 


@staff_required
def approved_income_transaction_total(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    try:
        start_date = date.fromisoformat(start_date_str) if start_date_str else date.today() - timedelta(days=30)
    except ValueError:
        start_date = date.today() - timedelta(days=30)

    try:
        end_date = date.fromisoformat(end_date_str) if end_date_str else date.today()
    except ValueError:
        end_date = date.today()

    total_amount = Transaction.objects.filter(
        status='APPROVED',
        voucher_date__range=(start_date, end_date)
    ).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'total_amount': total_amount
    }

    return render(request, 'transactions/approved_income_total.html', context)

@staff_required
def combined_payment_total(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    try:
        start_date = date.fromisoformat(start_date_str) if start_date_str else date.today() - timedelta(days=30)
    except ValueError:
        start_date = date.today() - timedelta(days=30)

    try:
        end_date = date.fromisoformat(end_date_str) if end_date_str else date.today()
    except ValueError:
        end_date = date.today()

    supplier_total = SupplierPayment.objects.filter(
        created_at__date__range=(start_date, end_date)
    ).aggregate(total=Sum('amount'))['total'] or 0

    menpower_total = MenPowerPayment.objects.filter(
        created_at__date__range=(start_date, end_date)
    ).aggregate(total=Sum('amount'))['total'] or 0

    grand_total = supplier_total + menpower_total

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'supplier_total': supplier_total,
        'menpower_total': menpower_total,
        'grand_total': grand_total
    }

    return render(request, 'transactions/payment_summary.html', context)



@staff_required
def transfer_view(request):
    if request.method == 'POST':
        sender_number = request.POST.get('sender_account_number')
        receiver_number = request.POST.get('receiver_account_number')
        amount = request.POST.get('amount')
        
        if sender_number == receiver_number:
            messages.error(request, "Sender and receiver cannot be the same account.")
            return redirect('transfer_view')  # or render with context if not using redirect 
        
        try:
            amount = int(amount)
            if amount <= 0:
                messages.error(request, "Amount must be greater than 0.")
                return redirect('transfer_view')

            with transaction.atomic():
                sender = BankAccount.objects.select_for_update().get(account_number=sender_number)
                receiver = BankAccount.objects.select_for_update().get(account_number=receiver_number)

                if sender.balance < amount:
                    messages.error(request, "Insufficient balance in sender account.")
                    return redirect('transfer_view')

                sender.balance -= amount
                receiver.balance += amount

                sender.save()
                receiver.save()

                messages.success(request, f"Successfully transferred {amount} from {sender.account_name} to {receiver.account_name}.")
                return redirect('transfer_view')

        except BankAccount.DoesNotExist:
            messages.error(request, "Invalid account number.")
        except ValueError:
            messages.error(request, "Invalid amount.")
        except Exception as e:
            messages.error(request, f"Unexpected error: {str(e)}")
        return redirect('transfer_view')

    accounts = BankAccount.objects.all()
    return render(request, 'transactions/transfer.html', {'accounts': accounts})
    
    
#হালত টাকা

@staff_required
def create_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Loan created successfully.")
            return redirect('loan_list_pending')
    else:
        form = LoanForm()
    return render(request, 'loan/create_loan.html', {'form': form})


# UPDATE Loan
@staff_required
def update_loan(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loan)
        if form.is_valid():
            form.save()
            messages.success(request, "Loan updated successfully.")
            return redirect('loan_list_pending')
    else:
        form = LoanForm(instance=loan)
    return render(request, 'loan/update_loan.html', {'form': form, 'loan': loan})


# LIST Loans with status = PENDING
@staff_required
def loan_list_pending(request):
    loans = Loan.objects.all().order_by('-created_at')
    return render(request, 'loan/loan_list_pending.html', {'loans': loans}) 


@staff_required
def mark_loan_as_paid(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)

    if loan.status == 'APPROVED':
        if loan.payment_amount >= loan.amount:
            loan.status = 'PAID'
            loan.save()
            messages.success(request, f"Loan from {loan.loan_provider_name} marked as PAID.")
        else:
            messages.warning(request, "Payment amount is less than loan amount. Cannot mark as PAID.")
    else:
        messages.warning(request, "Only APPROVED loans can be marked as PAID.")

    return redirect('loan_list_pending')


@staff_required
@transaction.atomic
def mark_loan_as_approved(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)

    if loan.status == 'PENDING':
        loan.status = 'APPROVED'
        loan.receive_date = timezone.now().date() 
        loan.save()

        # Bank balance update korbo jodi bank account thake
        if loan.bank_account:
            loan.bank_account.balance += loan.amount
            loan.bank_account.save()

        messages.success(request, f"Loan from {loan.loan_provider_name} marked as Approved and added to bank balance.")
    else:
        messages.warning(request, "Only PENDING loans can be marked as APPROVED.")

    return redirect('loan_list_pending')


@staff_required
@transaction.atomic
def create_payloan_view(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    payloans = loan.payments.all()

    if request.method == 'POST':
        form = PayLoanForm(request.POST)
        if form.is_valid():
            payloan = form.save(commit=False)
            payloan.loan = loan

            # Check
            if payloan.bank_account:
                if payloan.bank_account.balance < payloan.amount:
                    messages.error(request, "❌ Selected bank account does not have enough balance.")
                    return render(request, 'loan/create_payloan.html', {'form': form, 'loan': loan})
                
                
                payloan.bank_account.balance -= payloan.amount
                payloan.bank_account.save()
            else:
                return render(request, 'loan/create_payloan.html', {'form': form, 'loan': loan, 'payloans': payloans}) 
            
            payloan.save()

            # Update loan payment
            loan.payment_amount += payloan.amount
            if loan.payment_amount >= loan.amount:
                loan.status = 'PAID'
            loan.save()

            messages.success(request, "✅ Payment successfully recorded.")
            return redirect('loan_list_pending')
    else:
        form = PayLoanForm()

    return render(request, 'loan/create_payloan.html', {'form': form, 'loan': loan, 'payloans': payloans}) 


from django.db.models.functions import Greatest

@staff_required
def client_due_report(request):
    report = []

    companies = Company.objects.all()
    
    for company in companies:
        
        valid_projects = company.projects.filter(
            final_bill__isnull=False,
            final_bill__gt=0,
            status='RUNNING'
        ).annotate(
            due=ExpressionWrapper(
                F('final_bill') - F('current_paid'),
                output_field=IntegerField()
            )
        )
        
        # Aggregate total values
        total_final_bill = valid_projects.aggregate(total=Sum('final_bill'))['total'] or 0
        total_current_paid = valid_projects.aggregate(total=Sum('current_paid'))['total'] or 0
        total_due = valid_projects.aggregate(total=Sum('due'))['total'] or 0
        
        # Report e add koro, jodi kono project thake
        if valid_projects.exists():
            report.append({
                'name': company.name,
                'location': company.location,
                'phone': company.phone,
                'total_final_bill': total_final_bill,
                'total_current_paid': total_current_paid,
                'total_due': total_due
            })
        

    return render(request, 'reports/client_due_report.html', {'report': report})



@staff_required
def supplier_due_report(request):
    report = []

    suppliers = Supplier.objects.all()

    for supplier in suppliers:
        memos = supplier.memos.filter(is_payment_done=False)

        if memos.exists():
            total_amount = memos.aggregate(total=Sum('amount'))['total'] or 0
            total_paid = memos.aggregate(total=Sum('payment_balance'))['total'] or 0
            total_due = total_amount - total_paid

            report.append({
                'name': supplier.name,
                'location': supplier.location,
                'phone': supplier.phone,
                'total_amount': total_amount,
                'total_paid': total_paid,
                'total_due': total_due
            })

    return render(request, 'reports/supplier_due_report.html', {'report': report}) 



@staff_required
def devit_transaction_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    transactions = DevitTransactionHistory.objects.all().order_by('-created_at')


    if start_date and end_date:
        transactions = transactions.filter(created_at__date__range=[start_date, end_date])
    else:
        last_week = timezone.now() - timedelta(days=7)
        transactions = transactions.filter(created_at__gte=last_week)

    context = {
        'transactions': transactions,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'reports/devit_transaction_report.html', context)


@staff_required
def credit_transaction_report(request):

    today = date.today()
    default_start = today - timedelta(days=7)
    default_end = today

    start_date = request.GET.get('start_date', default_start)
    end_date = request.GET.get('end_date', default_end)

    # Convert to date objects if they're strings
    if isinstance(start_date, str):
        start_date = date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = date.fromisoformat(end_date)

    # Filter transactions
    transactions = Transaction.objects.filter(
        status = 'APPROVED',
        created_at__date__range=[start_date, end_date]
    ).select_related('project', 'company_account', 'bank')

    context = {
        'transactions': transactions,
        'start_date': start_date,
        'end_date': end_date,
        'total_amount': sum(t.amount for t in transactions)
    }
    return render(request, 'reports/credit_transaction_report.html', context)
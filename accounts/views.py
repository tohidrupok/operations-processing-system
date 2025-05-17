from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

from core.models import Project, Memo, ManpowerMemo, Record
from finance.models import Transaction
from django.db.models import Sum, F, ExpressionWrapper, IntegerField

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form}) 


def get_total_receivables_from_running_projects():
    receivables = Project.objects.filter(
        status='RUNNING',
        final_bill__gt=0  # Exclude 0 and None
    ).annotate(
        due=ExpressionWrapper(F('final_bill') - F('current_paid'), output_field=IntegerField())
    ).aggregate(
        total_due=Sum('due')
    )
    return receivables['total_due'] or 0 

def get_total_market_payables():
    payables = Memo.objects.annotate(
        due=ExpressionWrapper(F('amount') - F('payment_balance'), output_field=IntegerField())
    ).aggregate(
        total_due=Sum('due')
    )
    return payables['total_due'] or 0

def get_total_manpower_payables():
    payables = ManpowerMemo.objects.annotate(
        due=ExpressionWrapper(F('amount') - F('payment_balance'), output_field=IntegerField())
    ).aggregate(
        total_due=Sum('due')
    )
    return payables['total_due'] or 0 


@login_required
def home_view(request):

    if request.user.is_staff:
        projects = Project.objects.filter(status='RUNNING').count()
        all_projects = Project.objects.all().count()
        all_transaction= Transaction.objects.all().count()
        #record
        records = Record.objects.select_related('memo', 'manpower', 'project').order_by('-created_at')[:50]

        #pawna tk gula
        total_receivables = get_total_receivables_from_running_projects() 
        
        #dena tk gula
        total_market_due = get_total_market_payables()
        total_manpower_due = get_total_manpower_payables()
        total_all_due = total_market_due + total_manpower_due 
        
        context = {'projects': projects, 
                   'all_projects': all_projects,
                   'total_receivables': total_receivables,
                   'total_all_due':total_all_due,
                   'all_transaction': all_transaction, 
                   'records': records }
        
        return render(request, 'home_staff.html', context) 
    
    else:
        return render(request, 'home.html')
    
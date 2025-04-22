from django.shortcuts import render, get_object_or_404, redirect
from .models import Company, Supplier, MenPower
from .forms import CompanyForm, SupplierForm, MenPowerForm


# Company Views

def company_list(request):
    companies = Company.objects.all()
    return render(request, 'companie/company_list.html', {'companies': companies})

def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm()
    return render(request, 'companie/company_form.html', {'form': form})

def company_update(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'companie/company_form.html', {'form': form})

def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        company.delete()
        return redirect('company_list')
    return render(request, 'companie/company_confirm_delete.html', {'company': company})


# Supplier Views

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})

def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'supplier_form.html', {'form': form})

def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'supplier_form.html', {'form': form})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'supplier_confirm_delete.html', {'supplier': supplier})


# MenPower Views

def menpower_list(request):
    menpowers = MenPower.objects.all()
    return render(request, 'menpower_list.html', {'menpowers': menpowers})

def menpower_create(request):
    if request.method == 'POST':
        form = MenPowerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menpower_list')
    else:
        form = MenPowerForm()
    return render(request, 'menpower_form.html', {'form': form})

def menpower_update(request, pk):
    menpower = get_object_or_404(MenPower, pk=pk)
    if request.method == 'POST':
        form = MenPowerForm(request.POST, request.FILES, instance=menpower)
        if form.is_valid():
            form.save()
            return redirect('menpower_list')
    else:
        form = MenPowerForm(instance=menpower)
    return render(request, 'menpower_form.html', {'form': form})

def menpower_delete(request, pk):
    menpower = get_object_or_404(MenPower, pk=pk)
    if request.method == 'POST':
        menpower.delete()
        return redirect('menpower_list')
    return render(request, 'menpower_confirm_delete.html', {'menpower': menpower})

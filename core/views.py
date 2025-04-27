from django.shortcuts import render, get_object_or_404, redirect
from .models import Company, Supplier, MenPower, Category, Item
from .forms import CompanyForm, SupplierForm, MenPowerForm, CategoryForm, ItemForm


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
    return render(request, 'supplier/supplier_list.html', {'suppliers': suppliers})

def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'supplier/supplier_form.html', {'form': form})

def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'supplier/supplier_form.html', {'form': form})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'supplier/supplier_confirm_delete.html', {'supplier': supplier})


# MenPower Views

def menpower_list(request):
    menpowers = MenPower.objects.all()
    return render(request, 'menpower/menpower_list.html', {'menpowers': menpowers})

def menpower_create(request):
    if request.method == 'POST':
        form = MenPowerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menpower_list')
    else:
        form = MenPowerForm()
    return render(request, 'menpower/menpower_form.html', {'form': form})

def menpower_update(request, pk):
    menpower = get_object_or_404(MenPower, pk=pk)
    if request.method == 'POST':
        form = MenPowerForm(request.POST, request.FILES, instance=menpower)
        if form.is_valid():
            form.save()
            return redirect('menpower_list')
    else:
        form = MenPowerForm(instance=menpower)
    return render(request, 'menpower/menpower_form.html', {'form': form})

def menpower_delete(request, pk):
    menpower = get_object_or_404(MenPower, pk=pk)
    if request.method == 'POST':
        menpower.delete()
        return redirect('menpower_list')
    return render(request, 'menpower/menpower_confirm_delete.html', {'menpower': menpower})




# Category List
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})

# Category Create
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form})

# Category Update
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/category_form.html', {'form': form})

# Category Delete
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category/category_confirm_delete.html', {'category': category}) 


# Item List
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item/item_list.html', {'items': items})

# Item Create
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'item/item_form.html', {'form': form})

# Item Update
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'item/item_form.html', {'form': form})

# Item Delete
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'item/item_confirm_delete.html', {'item': item}) 

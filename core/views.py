from django.shortcuts import render, get_object_or_404, redirect
from .models import Company, Supplier, MenPower, Category, Item, Project, Memo, ManpowerMemo, Bank, Record
from .forms import CompanyForm, SupplierForm, MenPowerForm, CategoryForm, ItemForm,ProjectForm, MemoForm, ManpowerMemoForm, BankForm 

from django.contrib.auth.decorators import user_passes_test

def staff_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_staff)(view_func) 



# Company Views
@staff_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'companie/company_list.html', {'companies': companies})

@staff_required
def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm()
    return render(request, 'companie/company_form.html', {'form': form})


@staff_required
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


@staff_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        company.delete()
        return redirect('company_list')
    return render(request, 'companie/company_confirm_delete.html', {'company': company})


# Supplier Views


@staff_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier/supplier_list.html', {'suppliers': suppliers})


@staff_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'supplier/supplier_form.html', {'form': form})


@staff_required
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


@staff_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'supplier/supplier_confirm_delete.html', {'supplier': supplier})


# MenPower Views
@staff_required
def menpower_list(request):
    menpowers = MenPower.objects.all()
    return render(request, 'menpower/menpower_list.html', {'menpowers': menpowers})


@staff_required
def menpower_create(request):
    if request.method == 'POST':
        form = MenPowerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menpower_list')
    else:
        form = MenPowerForm()
    return render(request, 'menpower/menpower_form.html', {'form': form})

@staff_required
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


@staff_required
def menpower_delete(request, pk):
    menpower = get_object_or_404(MenPower, pk=pk)
    if request.method == 'POST':
        menpower.delete()
        return redirect('menpower_list')
    return render(request, 'menpower/menpower_confirm_delete.html', {'menpower': menpower})




# Category List
@staff_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})

# Category Create
@staff_required
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
@staff_required
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
@staff_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category/category_confirm_delete.html', {'category': category}) 


# Item List
@staff_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item/item_list.html', {'items': items})

# Item Create
@staff_required
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
@staff_required
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
@staff_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'item/item_confirm_delete.html', {'item': item}) 




# PROJECT CRUD
@staff_required
def project_list(request):
    projects = Project.objects.filter(status='RUNNING').order_by('-created_at')
    return render(request, 'project/project_list.html', {'projects': projects})


@staff_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project/project_form.html', {'form': form})


@staff_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project/project_form.html', {'form': form})


@staff_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'project/project_confirm_delete.html', {'project': project})

@staff_required
def project_record_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    records = Record.objects.filter(project=project).order_by('created_at')

    return render(request, 'project/project_record_detail.html', {
        'project': project,
        'records': records,
    })

# MEMO CRUD

@staff_required
def memo_list(request):
    memos = Memo.objects.all()
    return render(request, 'memo/memo_list.html', {'memos': memos})


@staff_required
def memo_create(request):
    if request.method == 'POST':
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            project = memo.project
            
            # Ensure current_cost is not None
            if project.current_cost is None:
                project.current_cost = 0

            # Add memo amount to project's current cost
            project.current_cost += memo.amount
            project.save()

            memo.save()
            form.save_m2m()  # For ManyToMany field 'items'
            
            
            Record.objects.create(
                memo=memo,
                project=project,
                amount=memo.amount,
            )

            return redirect('memo_list')

            return redirect('memo_list')
    else:
        form = MemoForm()
    return render(request, 'memo/memo_form.html', {'form': form})


@staff_required
def memo_update(request, pk):
    memo = get_object_or_404(Memo, pk=pk)
    if request.method == 'POST':
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            return redirect('memo_list')
    else:
        form = MemoForm(instance=memo)
    return render(request, 'memo/memo_form.html', {'form': form})


@staff_required
def memo_delete(request, pk):
    memo = get_object_or_404(Memo, pk=pk)
    if request.method == 'POST':
        memo.delete()
        return redirect('memo_list')
    return render(request, 'memo/memo_confirm_delete.html', {'memo': memo})

def memo_detail(request, pk):
    memo = get_object_or_404(Memo, pk=pk)
    return render(request, 'memo/memo_detail.html', {'memo': memo})




# MANPOWER MEMO CRUD
@staff_required
def manpowermemo_list(request):
    manpower_memos = ManpowerMemo.objects.all()
    return render(request, 'hiring/manpowermemo_list.html', {'manpower_memos': manpower_memos})


@staff_required
def manpowermemo_create(request):
    if request.method == 'POST':
        form = ManpowerMemoForm(request.POST)
        if form.is_valid():
            manpower_memo = form.save(commit=False)
            project = manpower_memo.project

            # Ensure current_cost is not None
            if project.current_cost is None:
                project.current_cost = 0

            # Add the manpower memo amount to current cost
            project.current_cost += manpower_memo.amount
            project.save()

            manpower_memo.save()
            
            Record.objects.create(
                manpower=manpower_memo,
                project=project,
                amount=manpower_memo.amount,
            ) 
                        
            return redirect('manpowermemo_list')
    else:
        form = ManpowerMemoForm()
    return render(request, 'hiring/manpowermemo_form.html', {'form': form})

@staff_required
def manpowermemo_update(request, pk):
    manpower_memo = get_object_or_404(ManpowerMemo, pk=pk)
    if request.method == 'POST':
        form = ManpowerMemoForm(request.POST, instance=manpower_memo)
        if form.is_valid():
            form.save()
            return redirect('manpowermemo_list')
    else:
        form = ManpowerMemoForm(instance=manpower_memo)
    return render(request, 'hiring/manpowermemo_form.html', {'form': form})


@staff_required
def manpowermemo_delete(request, pk):
    manpower_memo = get_object_or_404(ManpowerMemo, pk=pk)
    if request.method == 'POST':
        manpower_memo.delete()
        return redirect('manpowermemo_list')
    return render(request, 'hiring/manpowermemo_confirm_delete.html', {'manpower_memo': manpower_memo})

def manpowermemo_detail(request, pk):
    manpower_memo = get_object_or_404(ManpowerMemo, pk=pk)
    return render(request, 'hiring/manpowermemo_detail.html', {'manpower_memo': manpower_memo})

# Bank List
@staff_required
def bank_list(request):
    accounts = Bank.objects.all()
    total_balance = sum(account.balance for account in accounts)
    total_accounts = accounts.count()
    return render(request, 'bank/bank_list.html', {
        'accounts': accounts,
        'total_balance': total_balance,
        'total_accounts': total_accounts
    })

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


# Update
@staff_required
def bank_update(request, pk):
    account = get_object_or_404(Bank, pk=pk)
    if request.method == 'POST':
        form = BankForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('bank_list')
    else:
        form = BankForm(instance=account)
    return render(request, 'bank/bank_form.html', {'form': form})

# Delete
@staff_required
def bank_delete(request, pk):
    account = get_object_or_404(Bank, pk=pk)
    if request.method == 'POST':
        account.delete()
        return redirect('bank_list')
    return render(request, 'bank/bank_confirm_delete.html', {'account': account})
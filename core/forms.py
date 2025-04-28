from django import forms
from .models import Company, Supplier, MenPower, Category, Item, Project, Memo, ManpowerMemo

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class MenPowerForm(forms.ModelForm):
    class Meta:
        model = MenPower
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'image', 'category'] 
        
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = '__all__'

class ManpowerMemoForm(forms.ModelForm):
    class Meta:
        model = ManpowerMemo
        fields = '__all__'
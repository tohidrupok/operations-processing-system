from django import forms
from .models import Company, Supplier, MenPower

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

from django.contrib import admin
from .models import *


admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(Transaction)
admin.site.register(SupplierPayment)
admin.site.register(MenPowerPayment)
admin.site.register(Loan)
admin.site.register(PayLoan)
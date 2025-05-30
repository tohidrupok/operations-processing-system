from django.urls import path
from . import views

urlpatterns = [
    path('bank/list/', views.bank_list, name='bank_list'),
    path('bank/create/', views.bank_create, name='bank_create'),

    
    path('bank/account/list/', views.bank_accounts_list, name='bank_account_list'),
    path('bank/account/create/', views.bank_accounts_create, name='bank_account_create'),
    path('bank/account/edit/<int:pk>/', views.bank_accounts_update, name='bank_account_update'),
    
    
    path('pay/', views.transaction_list, name='transaction_list'),
    path('pay/create/', views.transaction_create, name='transaction_create'),
    path('pay/<int:pk>/update/', views.transaction_update, name='transaction_update'),
    path('pay/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    path('pay/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    path('transactions/<int:pk>/approve/', views.transaction_approve, name='transaction_approve'),
    
    #payment
    path('supplier-payment/create/', views.create_supplier_payment, name='create_supplier_payment'),
    path('supplier-payment/list/', views.supplier_payment_list, name='supplier_payment_list'),
    
    path('menpower-payment/create/', views.create_menpower_payment, name='create_menpower_payment'),
    path('menpower-payment/list/', views.menpower_payment_list, name='menpower_payment_list'),
    
    path('approved-total/', views.approved_income_transaction_total, name='approved_transaction_total'),
    path('payment-summary/', views.combined_payment_total, name='payment_summary'),
    path('transfer/', views.transfer_view, name='transfer_view'),
    
    
    path('loans/create/', views.create_loan, name='create_loan'),
    path('loans/<int:pk>/update/', views.update_loan, name='update_loan'),
    path('loans/pending/', views.loan_list_pending, name='loan_list_pending'),
    
    path('loan/<int:loan_id>/mark-paid/', views.mark_loan_as_paid, name='mark_loan_as_paid'),
    path('loan/<int:loan_id>/mark-approved/', views.mark_loan_as_approved, name='mark_loan_as_approved'),

    path('payloan/create/<int:loan_id>/', views.create_payloan_view, name='create_payloan'),
       
#repot    
    path('client-due-report/', views.client_due_report, name='client_due_report'),
    path('supplier-due-report/', views.supplier_due_report, name='supplier_due_report'),
    path('transaction-report/devit/', views.devit_transaction_report, name='devit_transaction_report'),
    path('transaction-report/credit/', views.credit_transaction_report, name='credit_transaction_report'),

]


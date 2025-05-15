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



]


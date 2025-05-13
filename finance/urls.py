from django.urls import path
from . import views

urlpatterns = [
    path('bank/list/', views.bank_list, name='bank_list'),
    path('bank/create/', views.bank_create, name='bank_create'),

    
    path('bank/account/list/', views.bank_accounts_list, name='bank_account_list'),
    path('bank/account/create/', views.bank_accounts_create, name='bank_account_create'),
    path('bank/account/edit/<int:pk>/', views.bank_accounts_update, name='bank_account_update'),



]


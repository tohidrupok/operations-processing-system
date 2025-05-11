from django.urls import path
from . import views

urlpatterns = [
    # Company URLs
    path('companies/', views.company_list, name='company_list'),
    path('companies/add/', views.company_create, name='company_create'),
    path('companies/<int:pk>/edit/', views.company_update, name='company_update'),
    path('companies/<int:pk>/delete/', views.company_delete, name='company_delete'),

    # Supplier URLs
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/edit/', views.supplier_update, name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),

    # MenPower URLs
    path('menpowers/', views.menpower_list, name='menpower_list'),
    path('menpowers/add/', views.menpower_create, name='menpower_create'),
    path('menpowers/<int:pk>/edit/', views.menpower_update, name='menpower_update'),
    path('menpowers/<int:pk>/delete/', views.menpower_delete, name='menpower_delete'),
    
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Item URLs
    path('items/', views.item_list, name='item_list'),
    path('items/create/', views.item_create, name='item_create'),
    path('items/<int:pk>/edit/', views.item_update, name='item_update'),
    path('items/<int:pk>/delete/', views.item_delete, name='item_delete'),  
    
    
    # Project
    path('projects/', views.project_list, name='project_list'),
    path('projects/all/', views.all_project_list, name='all_project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/update/<int:pk>/', views.project_update, name='project_update'),
    path('projects/delete/<int:pk>/', views.project_delete, name='project_delete'),
    path('project/<int:project_id>/records/', views.project_record_detail, name='project_record_detail'),
    path('project/<int:pk>/close/', views.close_project, name='close_project'),
    path('project/<int:pk>/make-final-bill/', views.make_final_bill, name='make_final_bill'),
    path('company/<int:company_id>/summary/', views.company_projects_summary, name='company_projects_summary'),



    # Memo
    path('memos/', views.memo_list, name='memo_list'),
    path('memos/create/', views.memo_create, name='memo_create'),
    path('memos/update/<int:pk>/', views.memo_update, name='memo_update'),
    path('memos/delete/<int:pk>/', views.memo_delete, name='memo_delete'),
    path('memo/<int:pk>/', views.memo_detail, name='memo_detail'),
    path('supplier/<int:supplier_id>/memos/', views.supplier_memo_summary, name='supplier_memo_summary'),


    # ManpowerMemo
    path('manpower-memos/', views.manpowermemo_list, name='manpowermemo_list'),
    path('manpower-memos/create/', views.manpowermemo_create, name='manpowermemo_create'),
    path('manpower-memos/update/<int:pk>/', views.manpowermemo_update, name='manpowermemo_update'),
    path('manpower-memos/delete/<int:pk>/', views.manpowermemo_delete, name='manpowermemo_delete'),
    path('manpowermemo/<int:pk>/', views.manpowermemo_detail, name='manpowermemo_detail'),
    path('worker/<int:worker_id>/manpowermemo/', views.worker_memo_summary, name='worker_memo_summary'),
    
     # bank
    path('bank/list/', views.bank_list, name='bank_list'),
    path('bank/create/', views.bank_create, name='bank_create'),
    path('bank/edit/<int:pk>/', views.bank_update, name='bank_update'),
    path('bank/delete/<int:pk>/', views.bank_delete, name='bank_delete'),

]


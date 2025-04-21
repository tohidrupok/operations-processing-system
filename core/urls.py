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
]


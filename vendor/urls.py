from django.urls import path
from vendor.views import *


urlpatterns = [
    path('vendors/create/', create_vendor, name='create_vendor'),
    path('vendors/', vendor_list, name='vendor_list'),
    path('vendors/detail/<int:pk>/', vendor_detail, name='vendor_detail'),


    path('transactions/create/', create_transaction, name='create_transaction'),
    path('transactions/', transaction_list, name='transaction_list'),
    path('transactions_detail/<int:pk>/', transaction_detail, name='transaction_detail'),
    path('transactions_edit/<int:pk>/', update_transaction, name='update_transaction'),
    path('transactions_delete/<int:pk>/', delete_transaction, name='delete_transaction'),
    
    path('generate-excel/', generate_excel, name='generate_excel'),

]
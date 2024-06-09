from django.urls import path
from .views import dashboard_home,inventory_view,add_producto,detail_product,delete_product,edit_product,clientes_view,add_cliente,detail_cliente,delete_cliente,edit_cliente 

urlpatterns = [
    path('dashboard', dashboard_home, name='dashboard-home'),
    
    path('inventory', inventory_view, name='inventory'),
    path('add-product', add_producto, name='add-product'),
    path('inventory/product/<int:pk>',detail_product,name='detail-product'),
    path('inventory/product/delete/<int:pk>',delete_product,name='delete-product'),
    path('inventory/product/edit/<int:pk>',edit_product,name='edit-product'),

    path('clients', clientes_view, name='clients'),
    path('add-clients', add_cliente, name='add-client'),
    path('clients/client/<int:pk>',detail_cliente,name='detail-client'),
    path('clients/client/delete/<int:pk>',delete_cliente,name='delete-cliente'),
    path('clients/client/edit/<int:pk>',edit_cliente,name='edit-cliente'),
]
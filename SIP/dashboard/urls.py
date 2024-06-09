from django.urls import path
from .views import dashboard_home,inventory_view,add_producto,detail_product,delete_product,edit_product 

urlpatterns = [
    path('dashboard', dashboard_home, name='dashboard-home'),
    path('inventory', inventory_view, name='inventory'),
    path('add-product', add_producto, name='add-product'),
    path('inventory/product/<int:pk>',detail_product,name='detail-product'),
    path('inventory/product/delete/<int:pk>',delete_product,name='delete-product'),
    path('inventory/product/edit/<int:pk>',edit_product,name='edit-product')
]
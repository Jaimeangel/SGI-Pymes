from django.urls import path
from .views import dashboard_home,inventory_view,add_producto,detail_product,delete_product,edit_product,clientes_view,add_cliente,detail_cliente,delete_cliente,edit_cliente 
from .views import proveedores_view,add_proveedor,detail_proveedor,delete_proveedor,edit_proveedor
from .views import orders_purchase_view,add_order_purchase,detail_order_purchase,delete_order_purchase,add_order_detail_purchase,delete_order_detail_purchase,edit_order_detail_purchase,complete_order_purchase
from .views import orders_sale_view,add_order_sale,detail_order_sale,delete_order_sale
from .views import add_order_detail_sale,delete_order_detail_sale,edit_order_detail_sale,complete_order_sale
from .views import informes_view,dashboard_products_sales,dashboard_products_purchase,dashboard_products_sales_registry_detail,dashboard_products_purchases_registry_detail


urlpatterns = [
    path('dashboard', dashboard_home, name='dashboard-home'),
    path('reports', informes_view, name='reports'),
    path('reports-sales-products', dashboard_products_sales, name='reports-sales-products'),
    path('reports-purchase-products', dashboard_products_purchase, name='reports-purchase-products'),


    path('reports-sale-by-product/<int:pk>', dashboard_products_sales_registry_detail, name='reports-sale-by-product'),
    path('reports-purchase-by-product/<int:pk>', dashboard_products_purchases_registry_detail, name='reports-purchase-by-product'),


    
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

    path('suppliers',proveedores_view , name='suppliers'),
    path('add-suppliers', add_proveedor, name='add-supplier'),
    path('suppliers/supplier/<int:pk>',detail_proveedor,name='detail-supplier'),
    path('suppliers/supplier/delete/<int:pk>',delete_proveedor,name='delete-supplier'),
    path('suppliers/supplier/edit/<int:pk>',edit_proveedor,name='edit-supplier'),

    #purchases
    path('order-purchase',orders_purchase_view , name='purchases'),
    path('add-order-purchase', add_order_purchase, name='add-order-purchase'),
    path('order-purchase/purchase/<int:pk>', detail_order_purchase, name='detail-order-purchase'),
    path('order-purchase/purchase/delete/<int:pk>', delete_order_purchase, name='delete-order-purchase'),

    path('add-order-detail-purchase/order/<int:pk>', add_order_detail_purchase, name='add-order-detail-purchase'),
    path('order-detail-purchase/delete/<int:pk>/order/<int:pk_order>', delete_order_detail_purchase, name='delete-order-detail-purchase'),
    path('order-detail-purchase/edit/<int:pk>/order/<int:pk_order>', edit_order_detail_purchase, name='edit-order-detail-purchase'),
    path('order-detail-purchase/complete/<int:pk>', complete_order_purchase, name='complete-order-detail-purchase'),

    #sales
    path('order-sale', orders_sale_view , name='sales'),
    path('add-order-sale', add_order_sale, name='add-order-sale'),
    path('order-sale/sale/<int:pk>', detail_order_sale, name='detail-order-sale'),
    path('order-sale/sale/delete/<int:pk>', delete_order_sale, name='delete-order-sale'),

    path('add-order-detail-sale/sale/<int:pk>', add_order_detail_sale, name='add-order-detail-sale'),
    path('order-detail-sale/delete/<int:pk>/sale/<int:pk_order>', delete_order_detail_sale, name='delete-order-detail-sale'),
    path('order-detail-sale/edit/<int:pk>/sale/<int:pk_order>', edit_order_detail_sale, name='edit-order-detail-sale'),
    path('order-detail-sale/complete/<int:pk>', complete_order_sale, name='complete-order-detail-sale')
    
]
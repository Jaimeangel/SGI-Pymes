from django.urls import path
from .views import dashboard_home,inventory_view 

urlpatterns = [
    path('dashboard', dashboard_home, name='dashboard-home'),
    path('inventory', inventory_view, name='inventory')
]
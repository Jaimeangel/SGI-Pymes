from django.urls import path
from .views import dashboard_home 

urlpatterns = [
    path('dashboard', dashboard_home, name='dashboard-home')
]
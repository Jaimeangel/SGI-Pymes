from django.contrib import admin

# Register your models here.
from .models import OrderSale,OrderSaleDetail

admin.site.register(OrderSale)
admin.site.register(OrderSaleDetail)

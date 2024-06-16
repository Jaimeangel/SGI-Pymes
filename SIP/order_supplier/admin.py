from django.contrib import admin

# Register your models here.
from .models import OrderSupplier,OrderSupplierDetail

admin.site.register(OrderSupplier)
admin.site.register(OrderSupplierDetail)

from django.db import models
from supplier.models import Supplier
from stock_product.models import Product

class OrderSupplier(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=255)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_total_value(self):
        total = sum(detail.quantity * detail.purchase_price for detail in self.ordersupplierdetail_set.all())
        self.total_value = total
        self.save()
    
    def __str__(self):
        return f"Order {self.id} - Client: {self.supplier}"

class OrderSupplierDetail(models.Model):
    order_supplier = models.ForeignKey(OrderSupplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order_supplier.update_total_value()

    def __str__(self):
        return f"Order Detail {self.id} - Supplier: {self.product.name}, Quantity: {self.quantity}, Sale Price: {self.purchase_price}"

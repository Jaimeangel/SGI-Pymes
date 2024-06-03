from django.db import models
from cliente.models import Client
from stock_product.models import Product

class OrderSale(models.Model):
    INPROGRESS = 'INPROGRESS'
    COMPLETED = 'COMPLETED'
    
    STATE_CHOICES = [
        (INPROGRESS, 'INPROGRESS'),
        (COMPLETED, 'COMPLETED'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(
        max_length=10,
        choices=STATE_CHOICES,
        default=INPROGRESS,
    )
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_total_value(self):
        total = sum(detail.quantity * detail.sale_price for detail in self.ordersaledetail_set.all())
        self.total_value = total
        self.save()

    def __str__(self):
        return f"Order {self.id} - Client: {self.client}"

class OrderSaleDetail(models.Model):
    order_sale = models.ForeignKey(OrderSale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)

    def save(self, *args, **kwargs):
        if not self.sale_price:
            self.sale_price = self.product.price_sale
        super().save(*args, **kwargs)
        self.order_sale.update_total_value()

    def __str__(self):
        return f"Order Detail {self.id} - Product: {self.product.name}, Quantity: {self.quantity}, Sale Price: {self.sale_price}"
        

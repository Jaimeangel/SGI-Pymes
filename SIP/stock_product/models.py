from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price_sale = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Check if the Stock instance exists, if not, create it
        if not hasattr(self, 'stock'):
            Stock.objects.create(product=self, current_stock=0)

    def __str__(self):
        return self.name

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    current_stock = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

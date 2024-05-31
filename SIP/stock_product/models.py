from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price_sale = models.DecimalField(max_digits=10, decimal_places=2)

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    current_stock = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)

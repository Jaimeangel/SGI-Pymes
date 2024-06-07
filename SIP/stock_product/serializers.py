from rest_framework import serializers
from .models import Category,Product,Stock

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # _all_ para obtener todos lo datos

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # _all_ para obtener todos lo datos

class StockSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = Stock
        fields = '__all__'  # _all_ para obtener todos lo datos
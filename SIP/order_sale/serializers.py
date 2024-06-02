from rest_framework import serializers
from .models import OrderSale,OrderSaleDetail

class OrderSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSale
        fields = '__all__'  # _all_ para obtener todos lo datos

class OrderSaleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSaleDetail
        fields = '__all__'  # _all_ para obtener todos lo datos

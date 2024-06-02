from rest_framework import serializers
from .models import OrderSupplier,OrderSupplierDetail

class OrderSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSupplier
        fields = '__all__'  # _all_ para obtener todos lo datos

class OrderSupplierDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSupplierDetail
        fields = '__all__'  # _all_ para obtener todos lo datos
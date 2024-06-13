from rest_framework import serializers
from .models import OrderSupplier,OrderSupplierDetail
from supplier.serializers import SupplierSerializer
from stock_product.serializers import ProductSerializer

class OrderSupplierWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSupplier
        fields = '__all__'

class OrderSupplierSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    class Meta:
        model = OrderSupplier
        fields = '__all__'  # _all_ para obtener todos lo datos

    def to_representation(self, instance):
        # Usar SupplierSerializer para la lectura
        representation = super().to_representation(instance)
        representation['supplier'] = SupplierSerializer(instance.supplier).data
        return representation

    def to_internal_value(self, data):
        # Usar OrderSupplierWriteSerializer para la escritura
        write_serializer = OrderSupplierWriteSerializer(data=data)
        write_serializer.is_valid(raise_exception=True)
        return write_serializer.validated_data


class OrderSupplierDetailWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSupplierDetail
        fields = '__all__'  # _all_ para obtener todos lo datos

class OrderSupplierDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderSupplierDetail
        fields = '__all__'  # _all_ para obtener todos lo datos
        read_only_fields = ["total_purchase"]
    
    def to_representation(self, instance):
        # Usar SupplierSerializer para la lectura
        representation = super().to_representation(instance)
        representation['product'] = ProductSerializer(instance.product).data
        return representation

    def to_internal_value(self, data):
        # Usar OrderSupplierWriteSerializer para la escritura
        write_serializer = OrderSupplierDetailWriteSerializer(data=data)
        write_serializer.is_valid(raise_exception=True)
        return write_serializer.validated_data
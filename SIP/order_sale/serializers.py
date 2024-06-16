from rest_framework import serializers
from .models import OrderSale,OrderSaleDetail
from cliente.serializers import ClientSerializer
from stock_product.serializers import ProductSerializer

class OrderSaleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSale
        fields = '__all__'

class OrderSaleSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    class Meta:
        model = OrderSale
        fields = '__all__'  # _all_ para obtener todos lo datos
    
    def to_representation(self, instance):
        # Usar SupplierSerializer para la lectura
        representation = super().to_representation(instance)
        representation['client'] = ClientSerializer(instance.client).data
        return representation

    def to_internal_value(self, data):
        # Usar OrderSupplierWriteSerializer para la escritura
        write_serializer = OrderSaleWriteSerializer(data=data)
        write_serializer.is_valid(raise_exception=True)
        return write_serializer.validated_data

class OrderSaleDetailWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSaleDetail
        fields = '__all__'

class OrderSaleDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderSaleDetail
        fields = '__all__'  # _all_ para obtener todos lo datos
        read_only_fields = ["total_detail"]

    def to_representation(self, instance):
        # Usar SupplierSerializer para la lectura
        representation = super().to_representation(instance)
        representation['product'] = ProductSerializer(instance.product).data
        return representation

    def to_internal_value(self, data):
        # Usar OrderSupplierWriteSerializer para la escritura
        write_serializer = OrderSaleDetailWriteSerializer(data=data)
        write_serializer.is_valid(raise_exception=True)
        return write_serializer.validated_data
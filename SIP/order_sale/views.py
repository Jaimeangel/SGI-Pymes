from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import OrderSale, OrderSaleDetail
from .serializers import OrderSaleSerializer,OrderSaleDetailSerializer

class OrderSaleViewSet(viewsets.ModelViewSet):
    queryset = OrderSale.objects.all()
    serializer_class = OrderSaleSerializer

    @action(detail=True, methods=['post'])
    def complete_order_sale(self, request, pk=None):
        try:
            order_sale = self.get_object()
        except OrderSale.DoesNotExist:
            return Response({"error": "OrderSale not found"}, status=status.HTTP_404_NOT_FOUND)

        if order_sale.state == OrderSale.COMPLETED:
            return Response({"error": "OrderSale is already completed"}, status=status.HTTP_400_BAD_REQUEST)

        # Update state to COMPLETED
        order_sale.state = OrderSale.COMPLETED
        order_sale.save()

        # Update stock for each OrderSaleDetail
        for detail in order_sale.ordersaledetail_set.all():
            product = detail.product
            product.stock.current_stock -= detail.quantity
            product.stock.save()

        return Response({"status": "OrderSale completed and stock updated successfully"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def order_details(self, request, pk=None):
        try:
            order_sale = self.get_object()
        except OrderSale.DoesNotExist:
            return Response({"error": "OrderSale not found"}, status=status.HTTP_404_NOT_FOUND)

        order_details = OrderSaleDetail.objects.filter(order_sale=order_sale)
        serializer = OrderSaleDetailSerializer(order_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def order_sale_by_product(self, request, pk=None):
        pass

class OrderSaleDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderSaleDetail.objects.all()
    serializer_class = OrderSaleDetailSerializer

    @action(detail=True, methods=['get'])
    def order_sale_by_product(self, request, pk=None):
        # Filtrar los OrderSaleDetail por producto (pk es el ID del producto)
        product_id = pk
        order_sale_details = OrderSaleDetail.objects.filter(product__id=product_id)
        
        # Serializar los datos
        serializer = self.get_serializer(order_sale_details, many=True)
        
        # Devolver la respuesta
        return Response(serializer.data)


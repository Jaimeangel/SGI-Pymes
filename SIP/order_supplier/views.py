from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import OrderSupplier,OrderSupplierDetail
from .serializers import OrderSupplierSerializer,OrderSupplierDetailSerializer

class OrderSupplierViewSet(viewsets.ModelViewSet):
    queryset = OrderSupplier.objects.all()
    serializer_class = OrderSupplierSerializer

    @action(detail=True, methods=['post'])
    def complete_order_purchase(self, request, pk=None):
        try:
            order_purchase = self.get_object()
        except OrderSupplier.DoesNotExist:
            return Response({"error": "OrderSale not found"}, status=status.HTTP_404_NOT_FOUND)

        if order_purchase.state == OrderSupplier.COMPLETED:
            return Response({"error": "OrderSale is already completed"}, status=status.HTTP_400_BAD_REQUEST)

        # Update state to COMPLETED
        order_purchase.state = OrderSupplier.COMPLETED
        order_purchase.save()

        
        # Update stock for each OrderSaleDetail
        for detail in order_purchase.ordersupplierdetail_set.all():
            product = detail.product
            product.stock.current_stock += detail.quantity
            product.stock.save()

        return Response({"status": "OrderSale completed and stock updated successfully"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def order_details(self, request, pk=None):
        try:
            order_supplier = self.get_object()
        except OrderSupplier.DoesNotExist:
            return Response({"error": "OrderSupplier not found"}, status=status.HTTP_404_NOT_FOUND)

        order_details = OrderSupplierDetail.objects.filter(order_supplier=order_supplier)
        serializer = OrderSupplierDetailSerializer(order_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderSupplierDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderSupplierDetail.objects.all()
    serializer_class = OrderSupplierDetailSerializer

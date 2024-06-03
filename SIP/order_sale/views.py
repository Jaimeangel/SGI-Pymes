from rest_framework import viewsets
from .models import OrderSale, OrderSaleDetail
from .serializers import OrderSaleSerializer,OrderSaleDetailSerializer

class OrderSaleViewSet(viewsets.ModelViewSet):
    queryset = OrderSale.objects.all()
    serializer_class = OrderSaleSerializer

class OrderSaleDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderSaleDetail.objects.all()
    serializer_class = OrderSaleDetailSerializer
from rest_framework import viewsets
from .models import OrderSupplier,OrderSupplierDetail
from .serializers import OrderSupplierSerializer,OrderSupplierDetailSerializer

class OrderSupplierViewSet(viewsets.ModelViewSet):
    queryset = OrderSupplier.objects.all()
    serializer_class = OrderSupplierSerializer

class OrderSupplierDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderSupplierDetail.objects.all()
    serializer_class = OrderSupplierDetailSerializer

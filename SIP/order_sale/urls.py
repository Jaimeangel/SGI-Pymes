from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderSaleDetailViewSet, OrderSaleViewSet

router = DefaultRouter()
router.register('sale', OrderSaleViewSet)
router.register('sale-details', OrderSaleDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
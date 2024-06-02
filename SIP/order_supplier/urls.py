from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import OrderSupplierViewSet,OrderSupplierDetailViewSet

router= DefaultRouter()
router.register('purchase',OrderSupplierViewSet)
router.register('purchase-detail',OrderSupplierDetailViewSet)

urlpatterns = [
    path('',include(router.urls))
]

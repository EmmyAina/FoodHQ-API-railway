from rest_framework import urlpatterns
from .views import OrderInformationViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', OrderInformationViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('', OrderTransaction.as_view(), name='order-from-cart')
]

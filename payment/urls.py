from rest_framework import urlpatterns
from .views import AppWalletViewset
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', AppWalletViewset)


urlpatterns = [
    path('', include(router.urls)),
]

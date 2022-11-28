from rest_framework import urlpatterns
from .views import AuthViewset
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', AuthViewset)

urlpatterns = [path('', include(router.urls))]

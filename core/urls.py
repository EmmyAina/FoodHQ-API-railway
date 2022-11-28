"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.conf.urls.static import static

base_url = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    # path(base_url + 'client/', include('client.urls')),
    path(base_url + 'order/', include('order.urls')),
    path(base_url + 'business/', include('business.urls')),
    path(base_url + 'auth/', include('authentication.urls')),
    path(base_url + 'payment/', include('payment.urls')),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]


schema_view = get_schema_view(
    openapi.Info(
        title="FoodHQ-API",
        default_version='v1',
        description="Eatry-API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ainae06@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)
urlpatterns += [
    path(base_url+'docs/', schema_view.with_ui('swagger',
                                               cache_timeout=0), name='schema-swagger-ui'),
    path(base_url+'redoc/', schema_view.with_ui('redoc',
                                                cache_timeout=0), name='schema-redoc'),
    # path('graphql/', csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=True)))
]

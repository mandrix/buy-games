from django.urls import path
from rest_framework.routers import DefaultRouter

from product.views import ProductPOSSimplifiedViewSet

router = DefaultRouter()

urlpatterns = [
    path("products/", ProductPOSSimplifiedViewSet.as_view({"get": "list"})),
]
urlpatterns += router.urls

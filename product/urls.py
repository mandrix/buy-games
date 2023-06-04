from django.urls import path

from product.views import ProductViewSet

urlpatterns = [
    path("product/", ProductViewSet.as_view({"post": "create", "get": "list"}))
]
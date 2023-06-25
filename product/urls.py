from django.urls import path

from product.views import ProductViewSet, CollectableViewSet, VideoGameViewSet, AccessoryViewSet
from .views import create_bills

urlpatterns = [
    path("product/", ProductViewSet.as_view({"post": "create", "get": "list"})),
    path("collectable/", CollectableViewSet.as_view({"post": "create", "get": "list"})),
    path("video-game/",  VideoGameViewSet.as_view({"post": "create", "get": "list"})),
    path("accessory/",  AccessoryViewSet.as_view({"post": "create", "get": "list"})),
    path('generar-factura/', create_bills, name='generar_factura'),
]
from django.urls import path

from product.views import ProductViewSet, CollectableViewSet, VideoGameViewSet, AccessoryViewSet

urlpatterns = [
    path("product/", ProductViewSet.as_view({"post": "create", "get": "list"})),
    path("collectable/", CollectableViewSet.as_view({"post": "create", "get": "list"})),
    path("video-game/",  VideoGameViewSet.as_view({"post": "create", "get": "list"})),
    path("accessory/",  AccessoryViewSet.as_view({"post": "create", "get": "list"})),

]
from django.urls import path

from product.views import ProductViewSet, CollectableViewSet, VideoGameViewSet, AccessoryViewSet

urlpatterns = [
    path("products/", ProductViewSet.as_view({"post": "create", "get": "list"})),
    path("product/<str:pk>/", ProductViewSet.as_view({"get": "retrieve"})),
    path("collectable/", CollectableViewSet.as_view({"post": "create", "get": "list"})),
    path("video-game/",  VideoGameViewSet.as_view({"post": "create", "get": "list"})),
    path("accessory/",  AccessoryViewSet.as_view({"post": "create", "get": "list"})),

]
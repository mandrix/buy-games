from rest_framework import viewsets

from product.models import Product, Collectable, VideoGame, Accessory
from product.serializer import ProductSerializer, CollectableSerializer, VideoGameSerializer, AccessorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter()
    serializer_class = ProductSerializer
    permission_classes = []


class CollectableViewSet(viewsets.ModelViewSet):
    queryset = Collectable.objects.filter()
    serializer_class = CollectableSerializer
    permission_classes = []


class VideoGameViewSet(viewsets.ModelViewSet):
    queryset = VideoGame.objects.filter()
    serializer_class = VideoGameSerializer
    permission_classes = []


class AccessoryViewSet(viewsets.ModelViewSet):
    queryset = Accessory.objects.filter()
    serializer_class = AccessorySerializer
    permission_classes = []

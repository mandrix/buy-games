from django.db.models import Q
from rest_framework import viewsets

from rest_framework.response import Response
from product.models import Product, Collectable, VideoGame, Accessory
from product.serializer import ProductSerializer, CollectableSerializer, VideoGameSerializer, AccessorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter()
    serializer_class = ProductSerializer
    permission_classes = []

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get("pk") if type(kwargs.get("pk")) == int else None
        instance = self.queryset.filter(Q(barcode=kwargs.get("pk")) | Q(pk=pk)).first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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

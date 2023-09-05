from django.db.models import Q, Sum
from rest_framework import viewsets

from rest_framework.response import Response
from product.models import Product, Collectable, VideoGame, Accessory, Report, StateEnum
from product.serializer import ProductSerializer, CollectableSerializer, VideoGameSerializer, AccessorySerializer, \
    ReportSerializer

from rest_framework import filters


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(state=StateEnum.available)
    serializer_class = ProductSerializer
    permission_classes = []

    def retrieve(self, request, *args, **kwargs):
        self.queryset = Product.objects.filter(state__in=[StateEnum.available, StateEnum.reserved])
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


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = super().get_queryset()

        date_param = self.request.query_params.get('date', None)
        if date_param:
            queryset = queryset.filter(date=date_param)

        return queryset.annotate(total_products=Sum('sale__products__sale_price'))

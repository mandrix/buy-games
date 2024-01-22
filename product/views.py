from django.db.models import Sum, Count, IntegerField
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response
from product.models import Product, Collectable, VideoGame, Accessory, Report, StateEnum, Sale
from product.serializer import ProductSerializer, CollectableSerializer, VideoGameSerializer, AccessorySerializer, \
    ReportSerializer
from django_filters import rest_framework as django_filters
from datetime import datetime

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import filters, status
from django.http import JsonResponse
from django.db.models.functions import Cast


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(state=StateEnum.available)
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = []

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        tags = self.request.query_params.get('tags')
        if not tags:
            return self.queryset

        tags = tags.split(",")
        return self.queryset.filter(tags__name__in=tags)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = Product.objects.filter(state__in=[StateEnum.available, StateEnum.reserved])
        pk = kwargs.get("pk")
        instance = None

        if pk is not None:
            if pk.isdigit():
                instance = self.queryset.filter(id=pk).first()

            if instance is None:
                instance = self.queryset.filter(barcode=pk).first()
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


class DailySalesReport(APIView):

    def post(self, request):
        start_date_str = request.data.get('start_date')
        end_date_str = request.data.get('end_date')

        if start_date_str and end_date_str:
            try:
                start_date = timezone.make_aware(datetime.strptime(start_date_str, "%Y-%m-%d"))
                end_date = timezone.make_aware(datetime.strptime(end_date_str, "%Y-%m-%d"))
            except ValueError:
                return Response(
                    {"error": "Las fechas proporcionadas no tienen el formato correcto (YYYY-MM-DD)."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            queryset = Sale.objects.filter(purchase_date_time__range=(start_date, end_date))
            queryset = queryset.values('purchase_date_time__date').annotate(
                total_sales=Count('id'),
                gross_total=Cast(Sum('gross_total'), output_field=IntegerField()),
                net_total=Cast(Sum('net_total'), output_field=IntegerField()),
            ).order_by('purchase_date_time__date')

            data = list(queryset)  # Convertir el QuerySet en una lista de diccionarios
            return JsonResponse(data, safe=False)
        else:
            return Response(
                {"error": "Debes proporcionar las fechas de inicio y fin (start_date y end_date) en los parámetros de consulta."},
                status=status.HTTP_400_BAD_REQUEST
            )


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

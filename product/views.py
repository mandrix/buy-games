from rest_framework import viewsets

from product.models import Product, Collectable, VideoGame, Accessory
from product.serializer import ProductSerializer, CollectableSerializer, VideoGameSerializer, AccessorySerializer
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template, render_to_string
from django.conf import settings
from xhtml2pdf import pisa
#from utils.creat_bills import creat_bills, obtener_datos_factura
from io import BytesIO
import os


def create_bills(facture):
    template = get_template('template/bill.html')
    context = {'facture': facture}

    html = template.render(context)

    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')

    if not pdf.err:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="factura.pdf"'

        response.write(result.getvalue())

        return response

    return HttpResponse('Error al generar la factura', status=500)


def obtener_datos_factura():
    # Datos ficticios de la factura
    factura = {
        'numero': 'FAC-001',
        'fecha': date.today(),
        'productos': [
            {'nombre': 'Videojuego 1', 'precio': 29.99},
            {'nombre': 'Coleccionable 2', 'precio': 12.50},
            {'nombre': 'Consola Retro', 'precio': 99.99},
        ],
        'total': 142.48  # Suma de los precios de los productos
    }

    return factura


def generate_bill(request):
    bill = obtener_datos_factura()

    response = create_bills(bill)

    return response


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

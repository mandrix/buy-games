from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa
from datetime import date


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

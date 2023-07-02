import datetime

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import TemplateView
from reportlab.pdfgen import canvas
from xhtml2pdf import pisa
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


class CountDownView(TemplateView):
    template_name = "coming-soon.html"


class ReceiptView(TemplateView):
    template_name = "receipt.html"


class GenerateBill(TemplateView):

    def get(self, request):
        # Obtener los datos de la factura
        invoice_number = 1
        invoice_date = "07/02/2023"

        request.data = {
            'store_name': "Ready Games",
            'store_address': "50 norte del parque central de Alajuela. Costado del museo Juan Santamaria.",
            'store_contact': "84599023",
            'customer_name': "john",
            'receipt_number': "3",
            'purchase_date': "hoy",
            'customer_name': "venta",
            'payment_method': "card",
            'subtotal': "1000",
            'taxes': "5000",
            'discounts': "2",
            'total_amount': "4000",
            'barcode': "1212121",
            'name': "consola ",
            'price': "12000",
            'products':
                [
                    {'barcode': '123456789', 'name': 'Product 1', 'price': 10.99},
                    {'barcode': '987654321', 'name': 'Product 2', 'price': 19.99},
                ]
        }

        store_name = request.data['store_name']
        store_address = request.data['store_address']
        store_contact = request.data['store_contact']
        customer_name = request.data['customer_name']
        payment_method = request.data['payment_method']

        products = request.data['products']

        subtotal = request.data['subtotal']
        taxes = request.data['taxes']
        discounts = request.data['discounts']
        total_amount = request.data['total_amount']

        # Crear el documento PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="bill.pdf"'

        # Ajustar el tamaño del lienzo al tamaño de la factura (por ejemplo, 3.5 pulgadas x 8.5 pulgadas)
        c = canvas.Canvas(response, pagesize=(3.5 * inch, 8.5 * inch))

        # Ajustar el tamaño y la posición de los elementos en el PDF
        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.5 * inch, 7.5 * inch, "Store Name:")
        c.setFont("Helvetica", 10)
        c.drawString(1.5 * inch, 7.5 * inch, store_name)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.5 * inch, 7.2 * inch, "Store Address:")
        c.setFont("Helvetica", 10)
        c.drawString(2 * inch, 7.2 * inch, store_address)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.5 * inch, 6.9 * inch, "Store Contact:")
        c.setFont("Helvetica", 10)
        c.drawString(2 * inch, 6.9 * inch, store_contact)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.5 * inch, 6.6 * inch, "Receipt Number:")
        c.setFont("Helvetica", 10)
        c.drawString(2 * inch, 6.6 * inch, str(invoice_number))

        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.5 * inch, 6.3 * inch, "Purchase Date:")
        c.setFont("Helvetica", 10)
        c.drawString(2 * inch, 6.3 * inch, invoice_date)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.5 * inch, 6 * inch, "Customer Name:")
        c.setFont("Helvetica", 10)
        c.drawString(2 * inch, 6 * inch, customer_name)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.5 * inch, 5.7 * inch, "Payment Method:")
        c.setFont("Helvetica", 10)
        c.drawString(2 * inch, 5.7 * inch, payment_method)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.5 * inch, 5.4 * inch, "Products:")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.5 * inch, 5.2 * inch, "Barcode")
        c.drawString(1.5 * inch, 5.2 * inch, "Name")
        c.drawString(2.5 * inch, 5.2 * inch, "Price")

        y = 5 * inch  # Posición vertical inicial para los productos
        for product in products:
            c.setFont("Helvetica", 10)
            c.drawString(0.5 * inch, y, product['barcode'])
            c.drawString(1.5 * inch, y, product['name'])
            c.drawString(2.5 * inch, y, str(product['price']))
            y -= 0.2 * inch  # Espacio entre cada producto

        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.5 * inch, y, "Subtotal:")
        c.setFont("Helvetica", 10)
        c.drawString(2.5 * inch, y, f"₡{subtotal}")

        y -= 0.2 * inch
        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.5 * inch, y, "Taxes:")
        c.setFont("Helvetica", 10)
        c.drawString(2.5 * inch, y, f"₡{taxes}")

        y -= 0.2 * inch
        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.5 * inch, y, "Discounts:")
        c.setFont("Helvetica", 10)
        c.drawString(2.5 * inch, y, f"₡{discounts}")

        y -= 0.2 * inch
        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.5 * inch, y, "Total Amount:")
        c.setFont("Helvetica", 10)
        c.drawString(2.5 * inch, y, f"₡{total_amount}")

        c.showPage()
        c.save()

        return response

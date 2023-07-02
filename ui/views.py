import datetime

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import TemplateView
from reportlab.pdfgen import canvas
from xhtml2pdf import pisa


class CountDownView(TemplateView):
    template_name = "coming-soon.html"


class ReceiptView(TemplateView):
    template_name = "receipt.html"


class GenerateBill(TemplateView):
    template_name = "bill.html"

    def generate_pdf(self, context):
        template = get_template(self.template_name)
        html = template.render(context)

        buffer = BytesIO()

        page_size = (2, 2)

        pisa.CreatePDF(html, dest=buffer, pagesize=page_size)

        buffer.seek(0)

        return buffer

    def get(self, request, *args, **kwargs):
        invoice_number = 1
        invoice_date = datetime.date.today()

        # info de ejemplo
        request.data = {
            'receipt_number': "1",
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
        context = {
            **request.data,
            'invoice_number': invoice_number,
            'invoice_date': invoice_date,
        }

        buffer = self.generate_pdf(context)

        response = HttpResponse(buffer, content_type='application/pdf')

        response['Content-Disposition'] = f'attachment; filename="invoice_{invoice_number}.pdf"'

        return response
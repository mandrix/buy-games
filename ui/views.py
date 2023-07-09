
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views import View
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import json
from babel.numbers import format_currency
from django.template.loader import render_to_string


class SamplePrintPdfView(TemplateView):
    template_name = "receipt-template.html"

    def formattedNumber(self, number):
        return str(format_currency(number, 'CRC', locale='es_CR'))

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        context = self.get_context_data(**kwargs)
        context['store_name'] = data['storeName']
        context['store_address'] = data['storeAddress']
        context['store_contact'] = data['storeContact']
        context['receipt_number'] = data['receiptNumber']
        context['purchase_date'] = data['purchaseDate']
        context['customer_name'] = data['customerName']
        context['payment_method'] = data['paymentMethod']
        context['items'] = data['items']
        items = []
        for item in data['items']:
            formatted_price = self.formattedNumber(item['price'])
            items.append({
                'id': item['id'],
                'name': item['name'],
                'price': formatted_price,
            })
        context['items'] = items
        context['subtotal'] = self.formattedNumber(data['subtotal'])
        context['taxes'] = self.formattedNumber(data['taxes'])
        context['discounts'] = self.formattedNumber(data['discounts'])
        context['total_amount'] = self.formattedNumber(data['totalAmount'])

        return self.render_to_response(context)


class CountDownView(TemplateView):
    template_name = "coming-soon.html"


class ReceiptView(TemplateView):
    template_name = "receipt.html"


class GenerateBill(TemplateView):
    template_name = "receipt-template.html"

    def formattedNumber(self, number):
        return str(format_currency(number, 'CRC', locale='es_CR'))

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        context = self.get_context_data(**kwargs)
        context['store_name'] = data['storeName']
        context['store_address'] = data['storeAddress']
        context['store_contact'] = data['storeContact']
        context['receipt_number'] = data['receiptNumber']
        context['purchase_date'] = data['purchaseDate']
        context['customer_name'] = data['customerName']
        context['payment_method'] = data['paymentMethod']
        context['items'] = data['items']
        items = []
        for item in data['items']:
            formatted_price = self.formattedNumber(item['price'])
            items.append({
                'id': item['id'],
                'name': item['name'],
                'price': formatted_price,
            })
        context['items'] = items
        context['subtotal'] = self.formattedNumber(data['subtotal'])
        context['taxes'] = self.formattedNumber(data['taxes'])
        context['discounts'] = self.formattedNumber(data['discounts'])
        context['total_amount'] = self.formattedNumber(data['totalAmount'])

        rendered_template = render_to_string(self.template_name, context)

        response = HttpResponse(rendered_template, content_type='text/html')

        response['Content-Disposition'] = 'inline; filename="bill.html"'
        response['Cache-Control'] = 'no-cache'
        return self.render_to_response(context)

import json

from babel.numbers import format_currency
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from helpers.qr import qrOptions, qrLinkOptions
from helpers.returnPolicy import returnPolicyOptions


class ReturnPolicyView(TemplateView):
    template_name = "return-policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t_param = self.request.GET.get('t')
        context['return_policy_text'] = returnPolicyOptions[int(t_param)]
        return context


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
        context['payment_details'] = data['paymentDetails']
        context['return_policy'] = qrOptions[data['returnPolicy']]
        context['qr_url'] = qrLinkOptions[data['returnPolicy']]
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

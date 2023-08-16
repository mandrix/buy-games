import json

import logging
from datetime import datetime

from babel.numbers import format_currency
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from helpers.qr import qrOptions, qrLinkOptions
from helpers.returnPolicy import returnPolicyOptions
from django.db import transaction
from product.models import Product, StateEnum, Sale, Report


class ReturnPolicyView(TemplateView):
    template_name = "return-policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t_param = kwargs.get('t')
        context['return_policy_text'] = returnPolicyOptions[int(t_param)]
        return context


class CountDownView(TemplateView):
    template_name = "coming-soon.html"


class ReceiptView(TemplateView):
    template_name = "receipt.html"


class GenerateBill(TemplateView):
    template_name = "receipt-template.html"

    SERVICE = "S"

    def formattedNumber(self, number):
        return str(format_currency(number, 'CRC', locale='es_CR'))

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        context = self.get_context_data(**kwargs)
        context['store_name'] = data['storeName']
        context['store_address'] = data['storeAddress']
        context['store_contact'] = data['storeContact']
        context['store_mail'] = data['storeMail']
        context['receipt_number'] = data['receiptNumber']
        context['purchase_date'] = data['purchaseDate']
        context['customer_name'] = data['customerName']
        context['customer_mail'] = data['customerMail']
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
                'status': "APARTADO" if item.get('reserved') else ""
            })
            if item['id'] != self.SERVICE:
                product = Product.objects.get(id=item['id'])
                product.sale_date = datetime.now()
                reserved = item.get('reserved')
                product.remaining -= int(item['price']) if reserved else product.remaining
                product.state = StateEnum.sold if reserved and product.remaining <= 0 else StateEnum.reserved
                product.save()
        context['items'] = items
        context['subtotal'] = self.formattedNumber(data['subtotal'])
        context['taxes'] = self.formattedNumber(data['taxes'])
        context['discounts'] = self.formattedNumber(data['discounts'])
        context['total_amount'] = self.formattedNumber(data['totalAmount'])

        rendered_template = render_to_string(self.template_name, context)

        response = HttpResponse(rendered_template, content_type='text/html')

        self.create_sale(data)

        try:
            self.enviar_factura_por_correo(rendered_template, data['customerMail'], data['returnPolicy'])
        except SendMailError as e:
            logging.error(f'Error al enviar el correo: {e}')

        response['Content-Disposition'] = 'inline; filename="bill.html"'
        response['Cache-Control'] = 'no-cache'
        return self.render_to_response(context)

    def create_sale(self, data):
        try:
            with transaction.atomic():
                today = datetime.today().date()
                report, created = Report.objects.get_or_create(date=today)
                warranty_type = returnPolicyOptions[data['returnPolicy']]

                sale = Sale.objects.create(
                    report=report,
                    warranty_type=warranty_type,
                    purchase_date_time=data['purchaseDate'],
                    payment_method=data['paymentMethod'],
                    subtotal=data['subtotal'],
                    discount=data['discounts'],
                    taxes=data['taxes'],
                    total=data['totalAmount'],
                    payment_details=data['paymentDetails'],
                    customer_name=data['customerName'],
                    customer_mail=data['customerMail'],
                )

                for item in data['items']:
                    product_id = item['id']
                    product = Product.objects.get(id=product_id)
                    sale.products.add(product)

                return sale
        except Exception as e:
            logging.error(f'Error al crear la venta: {e}')
            return None

    def enviar_factura_por_correo(self, factura_html, address, return_policy):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = 'readygamescr@gmail.com'
        smtp_password = 'dasieujszfbbvcew'

        remittent = 'readygamescr@gmail.com'
        destination = address

        message = MIMEMultipart()
        message['From'] = remittent
        message['To'] = f'{destination}'
        message['Subject'] = '¡Factura Ready Games🎮🕹️👾!'

        email_template_name = "return-policy.html"
        email_context = {
            'return_policy_text': returnPolicyOptions[return_policy],
        }

        rendered_email_template = render_to_string(email_template_name, email_context)

        message.attach(MIMEText(factura_html, 'html'))
        message.attach(MIMEText(rendered_email_template, 'html'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(remittent, destination, message.as_string())
            print('Correo enviado correctamente')
        except Exception as e:
            raise SendMailError(str(e))
        finally:
            server.quit()


class SendMailError(Exception):
    pass

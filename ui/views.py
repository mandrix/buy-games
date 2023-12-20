import json

import logging
from datetime import datetime
from openpyxl import Workbook

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from administration.models import Coupon, CouponTypeEnum
from helpers.payment import formatted_number, choices_payment
from helpers.qr import qrOptions, qrLinkOptions
from helpers.returnPolicy import return_policy_options
from django.db import transaction
from product.models import Product, StateEnum, Sale, Report, OwnerEnum, VideoGame, Collectable, Console, Accessory
from rest_framework.views import APIView
from rest_framework.response import Response


class ReturnPolicyView(TemplateView):
    template_name = "return-policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t_param = kwargs.get('t')
        context['return_policy_text'] = return_policy_options[int(t_param)]["desc"]
        return context


class CountDownView(TemplateView):
    template_name = "coming-soon.html"


class ReceiptView(TemplateView):
    template_name = "receipt.html"


class ReportView(TemplateView):
    template_name = "report.html"


class GenerateBill(TemplateView):
    template_name = "receipt-template.html"

    SERVICE = "S"

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
        context['receipt_comments'] = data['receiptComments']
        context['return_policy'] = qrOptions[data['returnPolicy']]
        context['qr_url'] = qrLinkOptions[data['returnPolicy']]
        if data.get('order'):
            items, items_remaining = self.create_order(data)
            data["items"] = items
        else:
            items, items_remaining = self.create_items_list(data)
        context['items_remaining'] = items_remaining
        context['items'] = items
        context['subtotal'] = formatted_number(data['subtotal'])
        if float(data['taxes']):
            context['taxes'] = formatted_number(data['taxes'])
        else:
            context['taxes'] = 0
        context['discounts'] = formatted_number(data['discounts'])
        context['total_amount'] = formatted_number(data['totalAmount'])

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
        with transaction.atomic():
            today = datetime.today().date()
            report, created = Report.objects.get_or_create(date=today)
            warranty_type = return_policy_options[data['returnPolicy']]["name"]
            net_total = float(data['discounts'])
            sale = Sale.objects.create(
                report=report,
                warranty_type=warranty_type,
                purchase_date_time=data['purchaseDate'],
                payment_method=data['paymentMethod'],
                subtotal=data['subtotal'],
                discount=data['discounts'],
                taxes=data['taxes'],
                gross_total=data['totalAmount'],
                payment_details=data['paymentDetails'],
                customer_name=data['customerName'],
                customer_mail=data['customerMail'],
            )

            for item in data['items']:
                product_id = item['id']
                if product_id != self.SERVICE:
                    product = Product.objects.get(id=product_id)
                    net_total += float(product.payment.net_price)
                    sale.products.add(product)
            sale.net_total = net_total
            sale.save()
            return sale

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
            'return_policy_text': return_policy_options[return_policy]["desc"],
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

    def create_items_list(self, data):  # aqui se enlistan los items para ser modificados debido a
        # su compra en la BD, luego para mostrarse en una factura
        items = []
        items_remaining = []
        for item in data['items']:
            formatted_price = formatted_number(item['price'])  # rework por
            # la nueva tabla
            items.append({
                'id': item['id'],
                'name': item['name'],
                'price': formatted_price,
                'status': "APARTADO" if item.get('reserved') else ""
            })
            if item['id'] != self.SERVICE:
                product = Product.objects.get(id=item['id'])
                product.sale_date = datetime.now()
                payment = product.payment
                reserved = item.get('reserved')
                if payment.remaining == payment.sale_price:  # al iniciar un pago con un producto, se le
                    # setea el metodo de pago y el costo nuevo si es el caso
                    pay = choices_payment(data['paymentMethod'], payment.sale_price)
                    payment.payment_method = pay["method"]
                    payment.sale_price = pay["price"]
                    payment.remaining = pay["price"]
                payment.remaining = max(0, payment.remaining - int(item['price']) if reserved else 0)
                if payment.remaining:
                    items_remaining.append({
                        'id': item['id'],
                        'name': item['name'],
                        'remaining': formatted_number(payment.remaining)
                    }
                    )
                product.state = StateEnum.sold if not reserved or payment.remaining <= 0 else StateEnum.reserved
                payment.save()
                product.save()

        return items, items_remaining

    def get_additional_info(self, additional_info):
        all_info = {
            "videoGame": {
                "additional_info": VideoGame.objects
            },
            "collectable": {
                "additional_info": Collectable.objects
            },
            "console": {
                "additional_info": Console.objects
            },
            "accessory": {
                "additional_info": Accessory.objects
            },
        }
        return all_info[additional_info]

    def create_order(self, data):  # aqui se crea un pedido, el proceso es el siguiente:
        # se recibe la informacion del item (price, name, el pago adelantado, paymentMethod)
        # luego se crea un producto deacuerdo a la informacion, se asigna los valores extras como fechas, etc,
        # al crearse  los valores automaticos como payment, agarramos el objeto payment
        # le seteamos el paymentMethod y lo guardamos
        # TODO al hacer el cambio de sale_price para tener el neto, tenemos que
        #  hacer algo para guardar el neto en los pedidos
        item_info = data['items'][0]
        price_total = item_info['price']
        part_paid = item_info['partPaid']
        additional_info = self.get_additional_info(item_info['additionalInfo'])
        item_remaining = []
        item = []
        formatted_price = formatted_number(part_paid)

        product = Product.objects.create(sale_price=price_total, sale_date=datetime.now(),
                                         state=StateEnum.reserved, order=False, description=item_info["name"])

        additional_info["additional_info"].create(title=item_info["name"], product=product)
        item.append({
            'id': product.id,
            'name': item_info['name'],
            'price': formatted_price,
            'status': "APARTADO"
        })

        payment = product.payment
        pay = choices_payment(data['paymentMethod'], payment.sale_price)
        payment.payment_method = pay["method"]
        payment.remaining = max(0, int(float(payment.remaining) - float(part_paid)))  # aqui en ves de price,
        # debe ser el pago de apartado que vendrá en una variable diferente
        item_remaining.append({
            'id': product.id,
            'name': item_info['name'],
            'remaining': formatted_number(payment.remaining)
        }
        )
        payment.save()
        product.save()

        return item, item_remaining


class CalculateTotalView(APIView):
    def post(self, request, format=None):
        data = request.data

        products_data = data.get('products', [])
        tax = data.get('tax', False)
        discounts = float(data.get('discounts', 0))
        coupon_code = Coupon.objects.filter(code__exact=data.get('coupon_code'))

        total = -discounts
        tax_total = 0
        sub_total = 0
        for product_data in products_data:
            price = float(product_data.get('price', 0))
            reserved = product_data.get('reserved', False)
            if reserved:
                total += price
                sub_total += price
                if tax:
                    tax_total += price * 0.13
                    sub_total -= tax_total
                break
            else:
                sub_total += price
                if tax:
                    taxed_price = price / 0.87
                    total += taxed_price
                    tax_total += taxed_price - price
                else:
                    total += price

        coupon_discount = None
        if coupon_code:
            coupon_code = coupon_code[0]
            amount = coupon_code.amount

            coupon_discount = round(amount if coupon_code.type == CouponTypeEnum.fixed else (amount/100) * sub_total, 2)

        response_data = {
            'subtotal': round(sub_total, 2) if not coupon_discount else round(sub_total - coupon_discount, 2),
            'tax': round(tax_total, 2),
            'total': round(total, 2) if not coupon_discount else round(total - coupon_discount, 2),
            'coupon_discount': coupon_discount
        }

        return Response(response_data)


class CalculatePayNewProduct(APIView):
    def post(self, request, format=None):
        data = request.data
        price = data.get('price', 0)
        payment_method = data.get('paymentMethod', "Sinpe")
        new_price = choices_payment(payment_method, price)["price"]
        response_data = {
            'price': round(float(new_price), 2)
        }

        return Response(response_data)


def generate_excel_report(request, fecha=None):
    if fecha:
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            fecha = datetime.today().strftime('%Y-%m-%d')
    else:
        fecha = datetime.today().strftime('%Y-%m-%d')

    today = fecha
    report = Report.objects.get_or_create(date=today)[0]
    sales = Sale.objects.filter(report=report)

    wb = Workbook()
    ws = wb.active

    ws.append(['Producto', 'Precio Vendido', "Total Tienda", "Recibido", "Faltante", "Dueño"])

    total_sales = 0.0
    total_tienda = 0.0
    total_remaining = 0.0

    for sale in sales:
        for product in sale.products.all():
            receive_price = product.sale_price
            remaining = 0
            if product.state == StateEnum.reserved:
                remaining = product.remaining
                receive_price = receive_price - remaining

            if product.owner == OwnerEnum.Business:
                parte_tienda = float(receive_price)
            else:
                parte_tienda = float(receive_price // 10)
            total_remaining += float(remaining)
            total_tienda += parte_tienda
            ws.append([product.__str__(), product.sale_price, parte_tienda, receive_price, remaining, product.owner])
        total_sales += float(sale.gross_total)

    ws.append(['Total de Ventas', total_sales, total_tienda, "--", total_remaining])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=reporte_{today}.xlsx'
    wb.save(response)

    return response


class SendMailError(Exception):
    pass

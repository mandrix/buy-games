import json

import logging
from datetime import datetime

from django.conf import settings
from django.shortcuts import redirect
from openpyxl import Workbook

from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from rest_framework import status

from administration.models import Coupon, CouponTypeEnum, Client, Setting
from helpers.payment import formatted_number, choices_payment
from helpers.returnPolicy import return_policy_options
from django.db import transaction
from product.models import Product, StateEnum, Sale, Report, OwnerEnum, VideoGame, Collectable, Console, Accessory, \
    SaleTypeEnum, PlatformEnum, Replacement
from rest_framework.views import APIView
from rest_framework.response import Response

from product.serializer import GenerateBillSerializer
from product.views import Throttling


class ReturnPolicyView(TemplateView):
    template_name = "return-policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t_param = kwargs.get('t')
        context['return_policy_text'] = return_policy_options[int(t_param)]['desc']
        return context


class HomePageView(APIView, Throttling):

    def get(self, request):
        return redirect("https://store.readygamescr.com")


class ReceiptView(TemplateView):
    template_name = "receipt.html"


class ReportView(TemplateView):
    template_name = "report.html"


class GenerateBill(TemplateView):
    template_name = "receipt-template.html"
    SERVICE = "S"
    sale: Sale = None

    def handle_post_logic(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON format."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = GenerateBillSerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        print("validated_data:", validated_data)  # TODO: remove all prints for logs
        context = self.get_context_data(**kwargs)
        context.update(validated_data)

        if validated_data.get('order'):
            items, items_remaining = self.create_order(validated_data)
            validated_data['items'] = items
            self.sale = self.create_sale(serializer)
        else:
            self.sale = self.create_sale(serializer)
            items, items_remaining = self.create_items_list(self.sale, serializer)

        print("Created sale:", self.sale)

        context['items_remaining'] = items_remaining
        context['items'] = items
        context['subtotal'] = formatted_number(validated_data['subtotal'])
        context['taxes'] = formatted_number(validated_data['taxes']) if float(validated_data['taxes']) else 0
        context['discounts'] = formatted_number(validated_data['discounts'])
        context['total_amount'] = formatted_number(validated_data['total_amount'])
        context['online_payment'] = serializer.online_payment

        rendered_template = render_to_string(self.template_name, context)

        try:
            GenerateBill.enviar_factura_por_correo(
                rendered_template,
                validated_data['customer_mail'],
                validated_data['return_policy']
            )
        except SendMailError as e:
            logging.error(f'Error al enviar el correo: {e}')

        response = HttpResponse(rendered_template, content_type='text/html')
        response['Content-Disposition'] = 'inline; filename="bill.html"'
        response['Cache-Control'] = 'no-cache'
        return response

    def post(self, request, *args, **kwargs):
        return self.handle_post_logic(request, *args, **kwargs)

    def create_sale(self, data: GenerateBillSerializer):
        with transaction.atomic():
            today = datetime.today().date()
            report, created = Report.objects.get_or_create(date=today)
            warranty_type = return_policy_options[data.return_policy]['name']
            net_total = -float(data.discounts)

            payment_details = data.payment_details or ""
            payment_details = f"{payment_details} - {data.customer_phone or ''}"

            receipt_comments = data.receipt_comments or ""

            platform = data.platform or PlatformEnum.Store
            if data.online_payment:
                platform = PlatformEnum.Online

            sale = Sale.objects.create(
                report=report,
                warranty_type=warranty_type,
                purchase_date_time=data.purchase_date,
                payment_method=data.payment_method,
                platform=platform,
                subtotal=data.subtotal,
                discount=data.discounts,
                taxes=data.taxes,
                gross_total=data.total_amount,
                payment_details=payment_details,
                receipt_comments=receipt_comments,
                customer_name=data.customer_name,
                customer_mail=data.customer_mail,
                shipping=data.shipping,
                client=GenerateBill.get_or_create_client(data),
                onvo_pay_payment_intent_id=data.onvo_pay_payment_intent_id or None  # To save None instead of ""
            )

            for item in data.items:
                product_id = item["id"]
                if product_id != self.SERVICE:
                    product = Product.objects.get(id=product_id)
                    sale.products.add(product)

                    payment = product.payment
                    if data.online_payment:
                        sale.type = SaleTypeEnum.Pending
                    elif item.get("reserved"):
                        sale.type = SaleTypeEnum.Reserve
                        payment.net_price = float(item["price"])
                        payment.save()
                    elif data.order:
                        sale.type = SaleTypeEnum.Request
                        payment.net_price = float(data.total_amount)
                        payment.save()
                    else:
                        sale.type = SaleTypeEnum.Purchase

                    net_total += float(payment.net_price)

                elif product_id == self.SERVICE:
                    net_total += float(item["price"])
                    sale.type = SaleTypeEnum.Repair

            sale.net_total = net_total
            sale.save()
            return sale

    @staticmethod
    def get_or_create_client(data: GenerateBillSerializer):
        if client := Client.objects.filter(email__iexact=data.customer_mail).first():
            if data.customer_phone:
                client.phone_number = data.customer_phone
            if data.customer_name:
                client.full_name = data.customer_name
            client.save()
            return client

        return Client.objects.create(
            full_name=data.customer_name,
            email=data.customer_mail,
            _id=data.id,
            phone_number=data.customer_phone or ""
        )

    @staticmethod
    def enviar_factura_por_correo(factura_html, address, return_policy):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = 'readygamescr@gmail.com'
        smtp_password = 'uihn utds dvwn hqgi'

        remittent = 'readygamescr@gmail.com'
        destination = address

        message = MIMEMultipart()
        message['From'] = remittent
        message['To'] = f'{destination}'
        message['Subject'] = '¡Factura Ready Games🎮🕹️👾!'

        email_template_name = "return-policy.html"
        email_context = {
            'return_policy_text': return_policy_options[return_policy]['desc'],
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

    def create_items_list(self, sale, data: GenerateBillSerializer):
        """List items for modification due to purchase in the database and display them on a receipt."""
        items = []
        items_remaining = []

        for item in data.items:
            formatted_price = formatted_number(item["price"])
            id_ = item["id"]

            items.append({
                "id": id_,
                "name": item["name"],
                "price": formatted_price,
                "status": "RESERVED" if item.get("reserved") else ""
            })

            if id_ != self.SERVICE:
                product = Product.objects.get(id=id_)
                print("Updating product:", product)  # TODO: remove all prints for logs
                product.sale_date = datetime.now()
                payment = product.payment
                reserved = item.get("reserved")

                # If the payment has not started yet, set the payment method and new cost
                if payment.remaining == payment.sale_price:
                    pay = choices_payment(data.payment_method, payment.sale_price)
                    payment.payment_method = pay["method"]
                    payment.sale_price = pay["price"]
                    payment.remaining = pay["price"]

                # Deduct payment if reserved
                payment.remaining = max(0, payment.remaining - int(item["price"]) if reserved else 0)

                # Track remaining payments
                if payment.remaining:
                    items_remaining.append({
                        "id": id_,
                        "name": item["name"],
                        "remaining": formatted_number(payment.remaining)
                    })

                # Update product state
                if data.online_payment:
                    product.state = StateEnum.pending
                elif not reserved or payment.remaining <= 0:
                    product.state = StateEnum.sold
                else:
                    product.state = StateEnum.reserved

                # If the product is fully paid, mark the sale as completed
                if product.state == StateEnum.reserved and not product.payment.remaining:
                    sale.payments_completed = True
                elif product.state == StateEnum.reserved and product.payment.remaining:
                    sale.payments_completed = False

                payment.save()
                product.save()
                sale.save()

                # If another product with the same barcode is hidden, make it available
                if next_product_to_show := Product.objects.filter(
                        barcode__exact=product.barcode, state=StateEnum.available, hidden=True
                ).first():
                    next_product_to_show.hidden = False
                    next_product_to_show.save()

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
            "replacement": {
                "additional_info": Replacement.objects
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
                                         state=StateEnum.reserved, order=False, description=item_info['name'])

        additional_info['additional_info'].create(title=item_info['name'], product=product)
        item.append({
            'id': product.id,
            'name': item_info['name'],
            'price': formatted_price,
            'status': "APARTADO"
        })

        payment = product.payment
        pay = choices_payment(data['payment_method'], payment.sale_price)
        payment.payment_method = pay['method']
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


class BuyOnline(TemplateView):
    template_name = "receipt-template.html"

    def post(self, request, *args, **kwargs):
        if not settings.ONLINE_PAYMENT or Setting.objects.first().disable_online_purchase:
            return JsonResponse(
                {"error": "Hubo un error con el sistema y no se hizo el cobro."},
                status=403
            )
        generate_bill_view = GenerateBill()
        response = generate_bill_view.handle_post_logic(request, *args, **kwargs)
        if generate_bill_view.sale:
            return JsonResponse(
                {"message": generate_bill_view.sale.pk}
            )
        return response


class CalculateTotalView(APIView, Throttling):
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


class CalculatePayNewProduct(APIView, Throttling):
    def post(self, request, format=None):
        data = request.data
        price = data.get('price', 0)
        payment_method = data.get('paymentMethod', "Sinpe")
        new_price = choices_payment(payment_method, price)['price']
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

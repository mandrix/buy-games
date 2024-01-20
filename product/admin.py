from functools import reduce
from io import BytesIO

from django.contrib import admin, messages
from django.contrib.admin import StackedInline
from django.db.models import Q
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from helpers.business_information import business_information
from helpers.payment import formatted_number
from product.filters import SoldFilter, TypeFilter, ConsoleTitleFilter, BelowThreshHoldFilter
from product.forms import SaleInlineForm
from product.models import Product, Collectable, Console, VideoGame, Accessory, Report, Sale, Log, \
    StateEnum, Expense, Payment, Tag, OwnerEnum, SaleTypeEnum
from django.utils.html import format_html
from django.template.loader import render_to_string
from helpers.qr import qrOptions, qrLinkOptions


class VideoGamesInline(StackedInline):
    model = VideoGame
    extra = 0
    min_num = 0
    max_num = 1


class CollectableInline(StackedInline):
    model = Collectable
    extra = 0
    min_num = 0
    max_num = 1


class ConsoleInline(StackedInline):
    model = Console
    extra = 0
    min_num = 0
    max_num = 1


class AccessoryInline(StackedInline):
    model = Accessory
    extra = 0
    min_num = 0
    max_num = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "__str__", "tipo", "console_type", "description", 'copies', "_state", "sale_price_formatted",
        "sale_price_with_card", "sale_price_with_tasa_0",
        'used_display', 'owner', 'etiquetas')
    model = Product
    list_filter = (SoldFilter, TypeFilter, BelowThreshHoldFilter,
                   ConsoleTitleFilter, 'used', 'creation_date', 'provider', 'owner', 'tags', )
    inlines = []
    search_fields = ["videogame__title", "barcode", "console__title", "accessory__title", "collectable__title",
                     "description"]
    search_help_text = "Busca usando el titulo del videojuego, consola, accesorio, colleccionable o el codigo de barra"
    readonly_fields = (
        "id",
        "creation_date",
        "modification_date",
        "payment_link"
    )
    exclude = ('remaining', 'payment')

    change_form_template = "overrides/change_form.html"
    change_list_template = "overrides/change_list.html"

    def used_display(self, obj):
        color = 'orange' if obj.used else 'blue'
        value = "usado" if obj.used else "nuevo"
        style = 'color: {}; border: 1px solid {}; padding: 4px; border-radius: 4px;'.format(color, color)

        return format_html('<span style="{}">{}</span>', style, value)

    used_display.short_description = 'Used'

    class Media:
        css = {
            'all': ('css/admin_styles.css',)
        }
        js = ('js/admin_scripts.js',)

    def get_exclude(self, request, obj=None):
        exclude = list(self.exclude)

        if obj:
            exclude.remove('remaining')

        return exclude

    def payment_link(self, obj):
        if obj.payment:
            link = format_html(
                f'<a href="/admin/product/payment/{obj.payment.id}/change/">{obj.payment}</a>'
            )
            return link
        else:
            return "N/A"

    def tipo(self, obj):
        try:
            return obj.get_product_type()
        except:
            return "ERROR no tiene tipo de producto"

    def _state(self, obj: Product):
        hex_colors = {
            StateEnum.available: "#70BF2B",
            StateEnum.sold: "#E70012",
            StateEnum.reserved: "#FCC10F"
        }
        return format_html(
            "<div style='padding: 0.5em; background-color: {}; color: #fff; border-radius: 0.25em;'>{}</div>",
            hex_colors[obj.state],
            obj.get_state_display()
        )

    def get_inlines(self, request, obj):
        if not obj:
            return [VideoGamesInline, ConsoleInline, AccessoryInline, CollectableInline]

        inline_instances = []
        if obj.videogame_set.first():
            inline_instances.append(VideoGamesInline)
        elif obj.console_set.first():
            inline_instances.append(ConsoleInline)
        elif obj.accessory_set.first():
            inline_instances.append(AccessoryInline)
        elif obj.collectable_set.first():
            inline_instances.append(CollectableInline)
        return inline_instances

    def vendido(self, obj):
        return format_html(
            '<img src="/static/admin/img/icon-{}.svg" alt="True">',
            "yes" if obj.sale_date else "no"
        )

    def etiquetas(self, obj: Product):
        styling = lambda color: "display: inline-block; padding: 0.5em; " \
                                f"background-color: {color}; color: #fff; border-radius: 0.25em;"
        tag = lambda name, color: f'<div style="{styling(color)}">{name}</div>'

        inner_tags = "".join([tag(t.name, t.color) for t in obj.tags.all()])
        html = f"<div id='product_tags'>{inner_tags}</div>",

        return mark_safe(html[0])
    etiquetas.short_description = "Etiquetas"

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)  # Start with initial readonly_fields

        if obj and obj.state == StateEnum.sold:
            readonly_fields.extend(
                ['amount', 'sale_price', 'remaining', 'barcode', 'provider_purchase_date', 'sale_date'])
        elif obj and obj.state == StateEnum.reserved:
            readonly_fields.extend(
                ['sale_price', 'remaining', 'barcode', 'provider_purchase_date', 'sale_date', 'amount'])
        elif obj and obj.state == StateEnum.available:
            readonly_fields.extend(['remaining', 'provider_purchase_date', 'sale_date'])

        return readonly_fields

    def response_change(self, request, obj: Product):
        if "_print_barcode" in request.POST:
            messages.add_message(request, messages.INFO, f"Descarga exitosa de la barra de codigo")
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="barcode_with_string.pdf"'

            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)

            data_string = str(obj.barcode)  # Customize this to extract the string data from your model
            c.drawString(10, 750, str(obj))
            c.drawString(30, 730, obj.barcode)

            barcode = code128.Code128(data_string, barWidth=1, barHeight=25)
            barcode.drawOn(c, 0, 700)

            c.showPage()

            c.save()
            pdf_data = buffer.getvalue()
            buffer.close()

            response.write(pdf_data)
            return response
        return super().response_change(request, obj)

    payment_link.allow_tags = True
    vendido.short_description = 'Vendido'
    tipo.short_description = 'Tipo de producto'


class ConsoleAdmin(admin.ModelAdmin):
    model = Console


class CollectableAdmin(admin.ModelAdmin):
    model = Collectable


class VideoGameAdmin(admin.ModelAdmin):
    model = VideoGame
    list_display = ["title", "console", "get_region"]
    list_filter = ("console", "product__region")
    search_fields = ["title"]

    @admin.display(description='Region')
    def get_region(self, obj):
        return obj.product.region


class AccessoryAdmin(admin.ModelAdmin):
    model = Accessory


class PaymentAdmin(admin.ModelAdmin):
    model = Payment


class SaleInline(admin.TabularInline):
    model = Sale
    extra = 0
    form = SaleInlineForm


class ReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'total', 'total_business', 'total_mauricio', 'total_joseph')
    ordering = ("-date",)
    inlines = [SaleInline]

    readonly_fields = ("total",)

    def total(self, report: Report):
        if not report: return 0
        return f"₡{sum([sale.net_total for sale in report.sale_set.all()]):,}"

    def _calculate_total_for(self, report: Report, owner: OwnerEnum):
        if not report: return 0
        field_keyword = 'payment__net_price'
        remaining_percentage = 0.9 if owner != OwnerEnum.Business else 1

        all_sales = report.sale_set.all()

        list_of_all_products = [
            list(
                sale.products.filter(owner__exact=owner).values(field_keyword)
            ) if sale.products.count() else [{field_keyword: sale.net_total if owner == OwnerEnum.Business else 0}] for sale in all_sales
        ]

        list_of_all_products = reduce(lambda a,b: a+b, list_of_all_products) if len(list_of_all_products) else [{field_keyword: 0}]
        list_of_all_products = [float(total.get(field_keyword))*remaining_percentage if total.get(field_keyword) else 0 for total in list_of_all_products]

        if owner == OwnerEnum.Business:

            list_of_other_owners_products = [
                list(sale.products.filter(~Q(owner__exact=owner)).values(field_keyword)) for sale in all_sales
            ]
            list_of_other_owners_products = reduce(lambda a,b: a+b, list_of_other_owners_products) if len(list_of_other_owners_products) else [{field_keyword: 0}]
            list_of_other_owners_products = [
                float(total.get(field_keyword))*0.1 if total.get(field_keyword) else 0 for total in list_of_other_owners_products
            ]
            list_of_all_products = [*list_of_all_products, *list_of_other_owners_products]


            # Add repairs and requests


        return f"₡{sum(list_of_all_products):,.2f}"

    def total_business(self, report: Report):
        return self._calculate_total_for(report, OwnerEnum.Business)

    def total_mauricio(self, report: Report):
        return self._calculate_total_for(report, OwnerEnum.Mauricio)

    def total_joseph(self, report: Report):
        return self._calculate_total_for(report, OwnerEnum.Joseph)


class SaleAdmin(admin.ModelAdmin):
    model = Sale

    exclude = ('products',)
    readonly_fields = (
        'creation_date_time',
        'receipt_products',
    )
    list_display = ("__str__", "customer_mail", "customer_name", "type")
    search_fields = ("customer_name", "customer_mail", "products__videogame__title", "payment_details",
                     "products__console__title", "products__accessory__title", "products__collectable__title")
    list_filter = ("type",)
    ordering = ("-creation_date_time",)

    change_form_template = "overrides/btn_sale.html"

    @staticmethod
    def format_product_string(product):
        return f"{str(product)} - ₡{product.sale_price:,} - {product.owner} - {product.barcode} - ID: {product.id} \n"

    def receipt_products(self, obj: Sale):
        products_string = [ self.format_product_string(product) for product in obj.products.all() ]
        return " ".join(products_string)

    def response_change(self, request, obj: Sale):
        if "_print_receipt" in request.POST:
            context = {'store_name': business_information["store_name"],
                       'store_address': business_information["store_address"],
                       'store_contact': business_information["store_contact"],
                       'store_mail': business_information["store_mail"],
                       'receipt_number': "", 'purchase_date': obj.purchase_date_time,
                       'customer_name': obj.customer_name, 'customer_mail': obj.customer_mail,
                       'payment_method': obj.payment_method,
                       'payment_details': obj.payment_details, 'receipt_comments': obj.payment_details,
                       'return_policy': qrOptions[1], 'qr_url': qrLinkOptions[1],
                       "discounts": formatted_number(obj.discount), "total_amount": formatted_number(obj.gross_total)
                       }

            items = []
            if obj.type == SaleTypeEnum.Repair:
                formatted_price = formatted_number(obj.gross_total)
                items.append({
                    'id': "S",
                    'name': "---Reparaciòn---",
                    'price': formatted_price
                })
            else:
                product = obj.products.all()[0]
                if product.state == StateEnum.reserved:
                    items.append({
                        'id': product.id,
                        'name': product.__str__(),
                        'price': formatted_number(product.payment.sale_price - product.payment.remaining),
                        'status': "APARTADO"
                    })

                    items_remaining = [{
                        'id': product.id,
                        'name': product.__str__(),
                        'remaining': formatted_number(product.payment.remaining)
                    }]

                    context['items_remaining'] = items_remaining
                else:
                    for item in obj.products.all():
                        formatted_price = formatted_number(item.payment.sale_price)
                        items.append({
                            'id': item.id,
                            'name': item.__str__(),
                            'price': formatted_price
                        })

            context['items'] = items
            context['subtotal'] = formatted_number(obj.subtotal)
            if float(obj.taxes):
                context['taxes'] = formatted_number(obj.taxes)
            else:
                context['taxes'] = 0
            rendered_template = render_to_string("receipt-template.html", context)

            response = HttpResponse(rendered_template, content_type='text/html')

            response['Content-Disposition'] = 'inline; filename="bill.html"'
            response['Cache-Control'] = 'no-cache'
            admin_url = f"https://readygamescr.com/admin/product/sale/{obj.id}/change/"
            js_script = f"""
                <form action="{admin_url}" method="GET" id="openAdminForm">
                    <input type="submit" style="display:none;">
                </form>
                <script type="text/javascript">
                    document.getElementById('openAdminForm').submit();
                    window.print()
                </script>
            """
            response.content = response.content.decode('utf-8').replace('</body>', js_script + '</body>').encode('utf-8')
            return response

        return super().response_change(request, obj)


class LogAdmin(admin.ModelAdmin):
    model = Log


class ExpenseAdmin(admin.ModelAdmin):
    model = Expense


class TagAdmin(admin.ModelAdmin):
    model = Tag


admin.site.register(Product, ProductAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Payment, PaymentAdmin)

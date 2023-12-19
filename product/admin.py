from io import BytesIO

from django.contrib import admin, messages
from django.contrib.admin import StackedInline
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from product.filters import SoldFilter, TypeFilter, ConsoleTitleFilter
from product.forms import SaleInlineForm
from product.models import Product, Collectable, Console, VideoGame, Accessory, Report, Sale, Log, \
    StateEnum, Expense, Payment, Tag
from django.utils.html import format_html


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
        'used', 'owner', 'etiquetas')
    model = Product
    list_filter = ('owner', SoldFilter, TypeFilter, ConsoleTitleFilter, 'creation_date', 'region', 'used', 'provider', 'tags')
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
    list_display = ('date', 'total')
    inlines = [SaleInline]

    readonly_fields = ("total",)

    def total(self, report: Report):
        if not report:
            return 0
        return f"₡{sum([sale.gross_total for sale in report.sale_set.all()]):,}"


class SaleAdmin(admin.ModelAdmin):
    model = Sale

    exclude = ('products',)
    readonly_fields = (
        'creation_date_time',
        'receipt_products'
    )

    @staticmethod
    def format_product_string(product):
        return f"{str(product)} - ₡{product.sale_price:,} - {product.owner} - {product.barcode} \n"

    def receipt_products(self, obj: Sale):
        products_string = [ self.format_product_string(product) for product in obj.products.all() ]
        return " ".join(products_string)

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

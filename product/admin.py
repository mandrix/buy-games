from django.contrib import admin
from django.contrib.admin import StackedInline
from django.db.models import Q
from django.forms import ModelForm

# Register your models here.
from product.models import Product, Collectable, Console, VideoGame, Accessory, ConsoleEnum, Report, Sale, Log, \
    StateEnum
from django.utils.html import format_html


class ConsoleTitleFilter(admin.SimpleListFilter):
    title = 'Console Title'  # Displayed filter title
    parameter_name = 'console_title'  # URL parameter name for the filter

    def lookups(self, request, model_admin):
        # Return a list of tuples representing the filter options
        # The first element in each tuple is the actual value to filter on,
        # and the second element is the human-readable option name
        return ConsoleEnum.choices

    def queryset(self, request, queryset):
        # Apply the filter to the queryset
        value = self.value()
        if value:
            return queryset.filter(Q(console__title=value) | Q(videogame__console=value) | Q(accessory__console=value))
        return queryset


class TypeFilter(admin.SimpleListFilter):
    title = 'Tipo'
    parameter_name = 'tipo'

    def lookups(self, request, model_admin):
        return (
            ('videogame', 'Videojuego'),
            ('console', 'Consola'),
            ('accessory', 'Accesorio'),
            ('collectable', 'Coleccionable'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'videogame':
            return queryset.filter(videogame__isnull=False)
        elif self.value() == 'console':
            return queryset.filter(console__isnull=False)
        elif self.value() == 'accessory':
            return queryset.filter(accessory__isnull=False)
        elif self.value() == 'collectable':
            return queryset.filter(collectable__isnull=False)


class SoldFilter(admin.SimpleListFilter):
    title = 'Se vendio'
    parameter_name = 'sold'

    def lookups(self, request, model_admin):
        # Devuelve las opciones de filtro y sus etiquetas
        return (
            ('vendido', ('Vendido')),
            ('no_vendido', ('No Vendido')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'vendido':
            return queryset.exclude(sale_date__isnull=True)
        elif self.value() == 'no_vendido':
            return queryset.exclude(sale_date__isnull=False)


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
        "__str__", "tipo", "console_type", "owner", "state", "sale_price_formatted", 'used', 'copies', 'description')
    model = Product
    list_filter = ('owner', SoldFilter, TypeFilter, ConsoleTitleFilter, 'creation_date', 'region', 'used', 'state')
    inlines = []
    search_fields = ["videogame__title", "barcode", "console__title", "accessory__title", "collectable__title",
                     "description"]
    search_help_text = "Busca usando el titulo del videojuego, consola, accesorio, colleccionable o el codigo de barra"
    readonly_fields = (
        "id",
        "creation_date",
        "modification_date",
    )
    exclude = ('remaining',)

    def get_exclude(self, request, obj=None):
        exclude = list(self.exclude)

        if obj:
            exclude.remove('remaining')

        return exclude

    def tipo(self, obj):
        try:
            return obj.get_product_type()
        except:
            return "ERROR no tiene tipo de producto"

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


class SaleInline(admin.TabularInline):
    model = Sale
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(SaleInline, self).get_formset(request, obj=obj, **kwargs)
        if obj:
            formset.form.base_fields['products'].choices.queryset = Sale.objects.filter(report=obj)
            formset.form.base_fields['products'].choices.field.queryset = Sale.objects.filter(report=obj)
        return formset


class ReportAdmin(admin.ModelAdmin):
    list_display = ('date',)
    inlines = [SaleInline]


class SaleAdmin(admin.ModelAdmin):
    model = Sale

    readonly_fields = (
        'creation_date_time',
    )


class LogAdmin(admin.ModelAdmin):
    model = Log


admin.site.register(Product, ProductAdmin)
admin.site.register(Console, ConsoleAdmin)
admin.site.register(Collectable, CollectableAdmin)
admin.site.register(VideoGame, VideoGameAdmin)
admin.site.register(Accessory, AccessoryAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Log, LogAdmin)

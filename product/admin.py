from django.contrib import admin
from django.contrib.admin import StackedInline
from django.forms import ModelForm

# Register your models here.
from product.models import Product, Collectable, Console, VideoGame, Accessory
from django.utils.html import format_html


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
    list_display = ("__str__", "tipo", "owner", "vendido", "sale_price")
    model = Product
    list_filter = ('owner', SoldFilter, TypeFilter)
    inlines = []
    search_fields = ["videogame__title", "barcode"]

    def tipo(self, obj):
        return obj.get_product_type()

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
            '<span style="background-color: {}; color: white;">{}</span>',
            "green" if obj.sale_date else "red",
            "SI" if obj.sale_date else "NO"
        )

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
        return obj.product.region.upper()


class AccessoryAdmin(admin.ModelAdmin):
    model = Accessory


admin.site.register(Product, ProductAdmin)
admin.site.register(Console, ConsoleAdmin)
admin.site.register(Collectable, CollectableAdmin)
admin.site.register(VideoGame, VideoGameAdmin)
admin.site.register(Accessory, AccessoryAdmin)

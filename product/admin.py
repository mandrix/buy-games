from django.contrib import admin

# Register your models here.
from product.models import Product, Collectable, Console, VideoGame, Accessory
from django.utils.html import format_html


class SoldFilter(admin.SimpleListFilter):
    title = ('Se vendio')
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


class VideoGamesForm(forms.ModelForm):
    class Meta:
        model = VideoGame
        fields = '__all__'

class ProductAdmin(admin.ModelAdmin):
    list_display = ("__str__", "tipo", "owner", "vendido", "sale_price")
    model = Product
    list_filter = ('owner', SoldFilter)
    inlines = []
    def tipo(self, obj):
        return obj.get_product_type()

    def get_inline_instances(self, request, obj=None):
        # Retorna los formularios en línea según la relación seleccionada
        inline_instances = []
        if obj and obj.relacion:
            if obj.product == 'Video Games':
                inline_instances.append(Relacion1Form)
            elif obj.relacion == 'relacion2':
                inline_instances.append(Relacion2Form)
            elif obj.relacion == 'relacion3':
                inline_instances.append(Relacion3Form)
            elif obj.relacion == 'relacion4':
                inline_instances.append(Relacion4Form)
        return inline_instances
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # Agrega los botones personalizados al contexto del formulario
        if extra_context is None:
            extra_context = {}
        extra_context['custom_buttons'] = True
        return super().changeform_view(request, object_id, form_url, extra_context)

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


class AccessoryAdmin(admin.ModelAdmin):
    model = Accessory


admin.site.register(Product, ProductAdmin)
admin.site.register(Console, ConsoleAdmin)
admin.site.register(Collectable, CollectableAdmin)
admin.site.register(VideoGame, VideoGameAdmin)
admin.site.register(Accessory, AccessoryAdmin)

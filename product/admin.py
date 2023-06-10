from django.contrib import admin

# Register your models here.
from product.models import Product, Collectable, Console, VideoGame, Accessory


class ProductAdmin(admin.ModelAdmin):
    model = Product


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

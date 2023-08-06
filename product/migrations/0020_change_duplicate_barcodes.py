from django.db import migrations
from product.models import VideoGame, Collectable, Console, Accessory


def forwards(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return
    models = [VideoGame, Collectable, Console, Accessory]
    for m in models:
        for item in m.objects.all():
            if m.objects.filter(product__barcode=item.product.barcode):
                item.product.generate_barcode()
                item.product.save()


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0019_save_all_products_to_handle_amount'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
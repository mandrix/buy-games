from django.db import migrations
from product.models import VideoGame, Collectable, Console, Accessory


def forwards(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return
    models = [VideoGame, Collectable, Console, Accessory]
    for m in models:
        [t.save() for t in m.objects.all()]


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0018_alter_product_provider_purchase_date_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
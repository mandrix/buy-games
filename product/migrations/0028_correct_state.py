from django.db import migrations
from product.models import Product, StateEnum


def forwards(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return
    for p in Product.objects.all():
        if not p.sale_date and not p.state in [StateEnum.available, StateEnum.sold, StateEnum.reserved]:
            p.state = StateEnum.available
            p.save()


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0027_alter_product_state'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]

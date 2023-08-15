from django.db import migrations
from product.models import Product, StateEnum


def forwards(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return
    for p in Product.objects.all():
        if p.sale_date and p.state != StateEnum.reserved:
            p.state = StateEnum.sold
            p.save()


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0028_correct_state'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]

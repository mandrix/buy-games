from django.db import migrations
from product.models import Product, StateEnum


def forwards(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0028_correct_state'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]

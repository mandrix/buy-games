# Generated by Django 4.2.2 on 2023-07-20 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_alter_accessory_console_alter_console_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(max_length=22, null=True, unique=False),
        ),
    ]

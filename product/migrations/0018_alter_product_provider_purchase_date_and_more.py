# Generated by Django 4.2.2 on 2023-08-06 06:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_alter_accessory_console_alter_console_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='provider_purchase_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='En colones', max_digits=8, null=True),
        ),
    ]

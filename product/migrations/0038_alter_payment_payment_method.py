# Generated by Django 4.2.2 on 2023-10-06 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0037_payment_product_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('tasa 0', 'T0'), ('card', 'Card'), ('cash', 'Cash'), ('na', 'N/A')], default='na', max_length=100, null=True),
        ),
    ]

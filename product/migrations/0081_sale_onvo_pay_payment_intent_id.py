# Generated by Django 4.2.2 on 2025-02-10 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0080_alter_product_state_alter_sale_platform_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='onvo_pay_payment_intent_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

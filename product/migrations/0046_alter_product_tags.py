# Generated by Django 4.2.2 on 2023-11-15 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0045_alter_product_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='products', to='product.tag'),
        ),
    ]

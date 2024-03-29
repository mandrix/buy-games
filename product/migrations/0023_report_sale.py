# Generated by Django 4.2.2 on 2023-08-10 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_alter_product_barcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('purchase', 'Purchase'), ('sale', 'Sale'), ('reserve', 'Reserve')], max_length=10)),
                ('warranty_type', models.CharField(choices=[('standard', 'Standard'), ('extended', 'Extended')], max_length=10)),
                ('purchase_date_time', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(max_length=50)),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='En colones', max_digits=8, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='En colones', max_digits=8, null=True)),
                ('taxes', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='En colones', max_digits=8, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='En colones', max_digits=8, null=True)),
                ('payment_details', models.TextField()),
                ('customer_name', models.CharField(default='Ready', max_length=100)),
                ('customer_mail', models.EmailField(default='readygamescr@gmail.com', max_length=254)),
                ('products', models.ManyToManyField(to='product.product')),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.report')),
            ],
        ),
    ]

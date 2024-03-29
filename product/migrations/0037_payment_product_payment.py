# Generated by Django 4.2.2 on 2023-10-04 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0036_expense'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('remaining', models.DecimalField(decimal_places=2, max_digits=8)),
                ('payment_method', models.CharField(blank=True, choices=[('tasa 0', 'T0'), ('card', 'Card'), ('sinpe', 'Sinpe'), ('cash', 'Cash'), ('na', 'N/A')], default='na', max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.payment'),
        ),
    ]

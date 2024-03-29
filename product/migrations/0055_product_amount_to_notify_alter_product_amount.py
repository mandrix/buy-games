# Generated by Django 4.2.2 on 2024-01-12 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0054_alter_accessory_console_alter_console_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='amount_to_notify',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='amount',
            field=models.PositiveIntegerField(default=1, help_text='Se generan copias si pones mas que uno'),
        ),
    ]

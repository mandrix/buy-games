# Generated by Django 4.2.2 on 2023-12-04 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0047_alter_accessory_console_alter_console_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='total_net',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='En colones', max_digits=8, null=True),
        ),
    ]

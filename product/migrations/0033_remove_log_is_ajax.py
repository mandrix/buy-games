# Generated by Django 4.2.2 on 2023-08-18 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0032_log'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='is_ajax',
        ),
    ]

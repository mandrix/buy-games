# Generated by Django 4.2.2 on 2023-12-16 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0047_alter_accessory_console_alter_console_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='notes',
            field=models.TextField(default='', help_text='Notas internas'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(default='Descripción que puede ver el cliente'),
        ),
    ]

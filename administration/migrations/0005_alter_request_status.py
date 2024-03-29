# Generated by Django 4.2.2 on 2023-11-16 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0004_alter_request_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('purchased', 'Purchased'), ('in_transit', 'In Transit'), ('in_transit_with_wfbox', 'In Transit with WfBox'), ('not_found', 'Not Found'), ('received', 'Received'), ('na', 'N/A')], default='purchased', max_length=100),
        ),
    ]

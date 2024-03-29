# Generated by Django 4.2.2 on 2023-11-16 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0003_request_items_request_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('purchased', 'Purchased'), ('in_transit', 'In Transit'), ('in_transit_with_wfbox', 'In Transit with WfBox'), ('not_found', 'Not Found'), ('received', 'Received'), ('na', 'N/A')], default='na', max_length=100),
        ),
        migrations.AlterField(
            model_name='request',
            name='wf_box_received_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

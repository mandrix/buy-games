from django.db import migrations

def create_initial_setting(apps, schema_editor):
    Setting = apps.get_model("administration", "Setting")
    if not Setting.objects.exists():  # Ensure it runs only if no instance exists
        Setting.objects.create(disable_online_purchase=True)

class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0013_setting'),
    ]

    operations = [
        migrations.RunPython(create_initial_setting),
    ]

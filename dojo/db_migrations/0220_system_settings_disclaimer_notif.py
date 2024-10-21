# Generated by Django 5.0.8 on 2024-09-12 18:22

from django.db import migrations


def copy_notif_field(apps, schema_editor):
    system_settings_model = apps.get_model('dojo', 'System_Settings').objects.get()
    if system_settings_model.disclaimer_notifications:
        system_settings_model.disclaimer_reports = system_settings_model.disclaimer_notifications
        system_settings_model.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0219_system_settings_disclaimer_notif'),
    ]

    operations = [
        migrations.RunPython(copy_notif_field),
    ]

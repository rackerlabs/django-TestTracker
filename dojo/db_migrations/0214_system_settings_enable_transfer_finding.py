# Generated by Django 4.1.13 on 2024-04-10 20:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dojo", "0213_system_settings_orphan_findings"),
    ]

    operations = [
        migrations.AddField(
            model_name="system_settings",
            name="enable_transfer_finding",
            field=models.BooleanField(
                default=False,
                help_text="Enable transfer of findings between different product types",
                verbose_name="Enable Transfer Finding",
            ),
        ),
    ]

# Generated by Django 4.1.13 on 2024-02-18 22:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dojo", "0212_alter_transfer_finding_notes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transfer_finding",
            name="notes",
            field=models.CharField(blank=True, max_length=2500, null=True),
        ),
    ]

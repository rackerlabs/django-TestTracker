# Generated by Django 4.1.13 on 2024-02-12 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dojo", "0199_transfer_finding_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transfer_finding",
            name="destination_product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dojo.product",
            ),
        ),
    ]

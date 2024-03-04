# Generated by Django 4.1.13 on 2024-03-01 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dojo", "0207_remove_transferfinding_severity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transferfindingfinding",
            name="engagement_related",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="engagement_related",
                to="dojo.finding",
            ),
        ),
        migrations.AlterField(
            model_name="transferfindingfinding",
            name="finding_related",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dojo.finding",
                verbose_name="finding_related",
            ),
        ),
    ]

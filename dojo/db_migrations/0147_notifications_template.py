# Generated by Django 3.2.11 on 2022-01-25 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0146_lead_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='template',
            field=models.BooleanField(default=False),
        ),
    ]

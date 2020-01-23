# Generated by Django 2.2.4 on 2020-01-23 08:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0022_auto_20200120_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finding',
            name='cvss',
            field=models.TextField(max_length=117, null=True, validators=[django.core.validators.RegexValidator(message="CVSS must be entered in format: 'AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H'", regex='^AV:[NALP]|AC:[LH]|PR:[UNLH]|UI:[NR]|S:[UC]|[CIA]:[NLH]')]),
        ),
        migrations.AlterField(
            model_name='finding_template',
            name='cvss',
            field=models.TextField(max_length=117, null=True, validators=[django.core.validators.RegexValidator(message="CVSS must be entered in format: 'AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H'", regex='^AV:[NALP]|AC:[LH]|PR:[UNLH]|UI:[NR]|S:[UC]|[CIA]:[NLH]')]),
        ),
    ]

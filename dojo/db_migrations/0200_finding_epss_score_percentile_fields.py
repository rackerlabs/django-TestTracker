# Generated by Django 4.1.13 on 2024-02-05 19:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0199_whitesource_to_mend'),
    ]

    operations = [
        migrations.AddField(
            model_name='finding',
            name='epss_percentile',
            field=models.FloatField(blank=True, help_text='Percentile for the EPSS score: the proportion of all scored vulnerabilities with the same or a lower EPSS score.', null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='EPSS percentile'),
        ),
        migrations.AddField(
            model_name='finding',
            name='epss_score',
            field=models.FloatField(blank=True, help_text='EPSS score representing the probability [0-1] of exploitation in the wild in the 30 days following score publication.', null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='EPSS value'),
        ),
        migrations.AddIndex(
            model_name='finding',
            index=models.Index(fields=['epss_score'], name='dojo_findin_epss_sc_e40540_idx'),
        ),
        migrations.AddIndex(
            model_name='finding',
            index=models.Index(fields=['epss_percentile'], name='dojo_findin_epss_pe_567499_idx'),
        ),
    ]

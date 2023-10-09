# Generated by Django 4.1.11 on 2023-10-05 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0190_system_settings_experimental_fp_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_type',
            name='environment_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='environment_manager', to='dojo.dojo_user'),
        ),
        migrations.AddField(
            model_name='product_type',
            name='environment_technical',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='environment_technical', to='dojo.dojo_user'),
        ),
        migrations.AddField(
            model_name='product_type',
            name='product_type_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='product_type_manager', to='dojo.dojo_user'),
        ),
        migrations.AddField(
            model_name='product_type',
            name='product_type_technical_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='product_type_technical_contact', to='dojo.dojo_user'),
        ),
    ]

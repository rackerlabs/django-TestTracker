# Generated by Django 2.2.17 on 2021-01-02 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dojo', '0075_import_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Type_Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(default=0)),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dojo.Product_Type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product_Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dojo.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='product_members', through='dojo.Product_Member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product_type',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='prod_type_members', through='dojo.Product_Type_Member', to=settings.AUTH_USER_MODEL),
        ),
    ]

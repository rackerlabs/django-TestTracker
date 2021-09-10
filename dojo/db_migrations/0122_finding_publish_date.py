from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dojo", "0121_user_restrict"),
    ]

    operations = [
        migrations.AlterField(
            model_name="finding",
            name="publish_date",
            field=models.CharField(
                null=True,
                blank=True,
                verbose_name="Publish date",
                help_text="Date when this vulnerability was made publicly available.",
            ),
        )
    ]

# Generated by Django 4.2.8 on 2024-11-02 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0053_remove_products_videos"),
    ]

    operations = [
        migrations.AddField(
            model_name="products",
            name="url_video",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]

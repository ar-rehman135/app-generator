# Generated by Django 4.2.8 on 2024-10-31 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0048_props"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="featured",
            field=models.BooleanField(default=False),
        ),
    ]

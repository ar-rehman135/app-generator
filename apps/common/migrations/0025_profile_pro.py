# Generated by Django 4.2.8 on 2024-06-04 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0024_profile_job_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pro',
            field=models.BooleanField(default=False),
        ),
    ]

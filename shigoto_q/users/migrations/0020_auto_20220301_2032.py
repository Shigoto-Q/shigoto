# Generated by Django 3.1.7 on 2022-03-01 20:32

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0019_auto_20220301_1833"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]

# Generated by Django 3.1.7 on 2022-02-26 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0015_remove_user_task"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscriber",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
            ],
        ),
    ]

# Generated by Django 3.1.7 on 2022-04-16 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kubernetes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deployment",
            name="metadata",
            field=models.TextField(null=True),
        ),
    ]

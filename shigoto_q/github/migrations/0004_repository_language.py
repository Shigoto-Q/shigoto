# Generated by Django 3.1.7 on 2021-06-22 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("github", "0003_auto_20210622_0031"),
    ]

    operations = [
        migrations.AddField(
            model_name="repository",
            name="language",
            field=models.CharField(default="", max_length=120),
        ),
    ]
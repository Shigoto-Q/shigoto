# Generated by Django 3.1.7 on 2021-04-22 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_celery_beat", "0015_edit_solarschedule_events_choices"),
        ("users", "0006_auto_20210422_1722"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="crontab",
            field=models.ManyToManyField(to="django_celery_beat.CrontabSchedule"),
        ),
    ]

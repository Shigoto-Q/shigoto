# Generated by Django 3.1.7 on 2022-03-05 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_celery_beat", "0015_edit_solarschedule_events_choices"),
        ("users", "0021_auto_20220303_1937"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="clocked",
            field=models.ManyToManyField(
                blank=True, to="django_celery_beat.ClockedSchedule"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="interval",
            field=models.ManyToManyField(
                blank=True, to="django_celery_beat.IntervalSchedule"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="solar",
            field=models.ManyToManyField(
                blank=True, to="django_celery_beat.SolarSchedule"
            ),
        ),
    ]

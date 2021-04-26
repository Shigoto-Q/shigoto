# Generated by Django 3.1.7 on 2021-04-22 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("django_celery_beat", "0015_edit_solarschedule_events_choices"),
        ("users", "0004_auto_20210419_1335"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="crontab",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="django_celery_beat.crontabschedule",
            ),
        ),
    ]

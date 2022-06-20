from django.core.exceptions import ValidationError
from django.db import models


class FavoriteSchedule(models.Model):
    name = models.CharField(max_length=256, default="", blank=True)
    description = models.TextField(default="", blank=True, null=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=False, blank=True
    )
    interval = models.ForeignKey(
        "django_celery_beat.IntervalSchedule",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    clocked = models.ForeignKey(
        "django_celery_beat.ClockedSchedule",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    crontab = models.ForeignKey(
        "django_celery_beat.CrontabSchedule",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    solar = models.ForeignKey(
        "django_celery_beat.SolarSchedule",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def validate_unique(self, *args, **kwargs):
        super().validate_unique(*args, **kwargs)

        schedule_types = ["interval", "crontab", "solar", "clocked"]
        selected_schedule_types = [s for s in schedule_types if getattr(self, s)]

        if len(selected_schedule_types) == 0:
            raise ValidationError(
                "One of clocked, interval, crontab, or solar " "must be set."
            )

        err_msg = "Only one of clocked, interval, crontab, " "or solar must be set"
        if len(selected_schedule_types) > 1:
            error_info = {}
            for selected_schedule_type in selected_schedule_types:
                error_info[selected_schedule_type] = [err_msg]
            raise ValidationError(error_info)

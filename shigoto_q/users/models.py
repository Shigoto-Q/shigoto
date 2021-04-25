from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import (
    PeriodicTask,
    CrontabSchedule,
    IntervalSchedule,
    ClockedSchedule,
    SolarSchedule,
)


class User(AbstractUser):
    first_name = models.CharField(max_length=256, default="")
    last_name = models.CharField(max_length=256, default="")
    company = models.CharField(max_length=100, default="")
    country = models.CharField(max_length=250, default="")
    city = models.CharField(max_length=250, default="")
    state = models.CharField(max_length=250, default="")
    zip_code = models.IntegerField(default=1000)
    customer = models.ForeignKey(
        "djstripe.Customer",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Stripe Customer Object"),
    )
    subscription = models.ForeignKey(
        "djstripe.Subscription",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Stripe Subscripton Object"),
    )
    total_tasks = models.IntegerField(default=0)
    crontab = models.ManyToManyField(CrontabSchedule)
    interval = models.ManyToManyField(IntervalSchedule)
    task = models.ManyToManyField(PeriodicTask)
    clocked = models.ManyToManyField(ClockedSchedule)
    solar = models.ManyToManyField(SolarSchedule)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)

from shigoto_q.github.models import GitHubProfile


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=256, default="")
    last_name = models.CharField(max_length=256, default="")
    email = models.CharField(
        _("email"),
        max_length=250,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    company = models.CharField(max_length=100, default="", null=True, blank=True)
    country = models.CharField(max_length=250, default="", null=True, blank=True)
    city = models.CharField(max_length=250, default="", null=True, blank=True)
    state = models.CharField(max_length=250, default="", null=True, blank=True)
    zip_code = models.IntegerField(default=1000, null=True, blank=True)
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
    crontab = models.ManyToManyField(CrontabSchedule, blank=True)
    interval = models.ManyToManyField(IntervalSchedule, blank=True)
    clocked = models.ManyToManyField(ClockedSchedule, blank=True)
    solar = models.ManyToManyField(SolarSchedule, blank=True)
    github = models.OneToOneField(
        GitHubProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.first_name


class Subscriber(models.Model):
    email = models.EmailField()

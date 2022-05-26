import datetime

from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    PermissionsMixin,
    UserManager,
)
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


class User(AbstractBaseUser, PermissionsMixin):
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
    is_staff = models.BooleanField(default=False)
    two_factor_auth_enabled = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)
    total_active_deployments = models.IntegerField(default=0)
    total_active_services = models.IntegerField(default=0)
    total_active_namespaces = models.IntegerField(default=0)
    active_ingress = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.first_name

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name


class Subscriber(models.Model):
    email = models.EmailField()


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="teams", through="Membership")
    subscription = models.ForeignKey(
        "djstripe.Subscription",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="The team's Stripe Subscription object, if it exists",
    )


class Membership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        "djstripe.Customer",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="The member's Stripe Customer object for this team, if it exists",
    )

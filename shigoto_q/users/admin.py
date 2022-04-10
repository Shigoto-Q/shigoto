from django.contrib import admin
from django.contrib.auth import get_user_model
from shigoto_q.users.models import Subscriber

User = get_user_model()


@admin.register(Subscriber)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ("email",)
    list_filter = ("email",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_login",
        "is_superuser",
        "first_name",
        "last_name",
        "email",
        "company",
        "country",
        "city",
        "state",
        "zip_code",
        "customer",
        "subscription",
        "github",
        "is_staff",
    )
    list_filter = (
        "last_login",
        "is_superuser",
        "customer",
        "subscription",
        "github",
        "is_staff",
    )
    raw_id_fields = (
        "groups",
        "user_permissions",
        "crontab",
        "interval",
        "clocked",
        "solar",
    )

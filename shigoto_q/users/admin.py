from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from shigoto_q.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    filter_horizontal = [
        "crontab",
        "task",
        "interval",
        "groups",
        "user_permissions",
        "clocked",
        "solar",
    ]
    raw_id_fields = ["customer", "subscription"]
    fieldsets = (
        (
            _("User info"),
            {
                "fields": (
                    "github",
                    "username",
                    "first_name",
                    "last_name",
                    "company",
                    "country",
                    "zip_code",
                    "state",
                    "city",
                    "password",
                )
            },
        ),
        (_("Stripe/Payment info"), {"fields": ("subscription", "customer")}),
        (_("Tasks"), {"fields": ("crontab", "interval", "clocked", "solar", "task")}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "first_name", "customer", "subscription"]
    search_fields = ["name"]

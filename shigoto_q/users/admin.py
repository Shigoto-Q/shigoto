from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import UserTasks
from shigoto_q.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(UserTasks)
class UserTasksAdmin(admin.ModelAdmin):
    list_display = ("id", "task")
    list_filter = ("task",)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "company",
                    "password",
                    "subscription",
                    "customer",
                )
            },
        ),
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
    list_display = ["username", "first_name", "total_tasks", "customer", "subscription"]
    search_fields = ["name"]

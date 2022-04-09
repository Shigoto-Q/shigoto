from django.contrib import admin
from django.contrib.auth import get_user_model
from shigoto_q.users.models import Subscriber

User = get_user_model()


@admin.register(Subscriber)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = (
        "email",
    )
    list_filter = ("email",)

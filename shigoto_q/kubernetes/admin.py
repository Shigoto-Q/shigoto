from django.contrib import admin

from shigoto_q.kubernetes.models import Deployment


@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display = ("id", "external_id", "kind", "image", "name", "metadata")
    list_filter = ("image",)
    search_fields = ("name",)

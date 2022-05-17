from django.contrib import admin

from shigoto_q.kubernetes.models import Deployment, Ingress, Service


@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "external_id",
        "kind",
        "image",
        "name",
        "metadata",
        "yaml",
    )
    list_filter = ("image",)
    search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "external_id",
        "type",
        "name",
        "namespace",
        "metadata",
        "port",
        "target_port",
        "yaml",
    )
    search_fields = ("name",)


@admin.register(Ingress)
class IngressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "external_id",
        "name",
        "host",
        "metadata",
        "path",
        "path_type",
        "yaml",
    )
    search_fields = ("name",)

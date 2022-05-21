from django.contrib import admin

from shigoto_q.kubernetes.models import Deployment, Ingress, Service, Namespace, Config


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


@admin.register(Namespace)
class NamespaceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "ingress", "user")
    list_filter = ("ingress", "user")
    raw_id_fields = ("deployments", "services")
    search_fields = ("name",)


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "user")
    list_filter = ("user",)

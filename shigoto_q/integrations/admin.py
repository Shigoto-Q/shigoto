from django.contrib import admin

from shigoto_q.integrations.models import (
    WebhookIntegration,
    WebhookObserver,
    WebhookEvent,
)


@admin.register(WebhookIntegration)
class WebhookIntegrationAdmin(admin.ModelAdmin):
    list_display = ("id", "url", "name", "type", "user")
    search_fields = ("name",)


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(WebhookObserver)
class WebhookObserverAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "webhook")
    list_filter = ("user", "webhook")
    search_fields = ("name",)

from django.contrib import admin

from .models import FeatureFlag


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = ("id", "definition", "description", "enabled")
    list_filter = ("enabled",)
    raw_id_fields = ("users",)

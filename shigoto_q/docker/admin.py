from django.contrib import admin

from shigoto_q.docker.models import DockerImage


@admin.register(DockerImage)
class DockerImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "repository",
        "name",
        "image_name",
        "command",
        "user",
    )

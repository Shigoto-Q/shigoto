from django.contrib import admin

from shigoto_q.horizon.models import Database


@admin.register(Database)
class DatabaseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'engine',
        'host',
        'port',
        'name',
        'username',
        'password',
    )
    search_fields = ('name',)

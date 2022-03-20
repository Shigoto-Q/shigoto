from django.contrib import admin

from .models import FavoriteSchedule


@admin.register(FavoriteSchedule)
class FavoriteScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'user',
        'interval',
        'clocked',
        'crontab',
        'solar',
    )
    list_filter = ('user', 'interval', 'clocked', 'crontab', 'solar')
    search_fields = ('name',)

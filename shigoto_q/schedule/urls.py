from django.urls import path

from shigoto_q.schedule import views

app_name = "schedule"

urlpatterns = [
    path(
        "/schedule/crontab/create/",
        views.CrontabScheduleCreateView.as_view(),
        name="schedule.crontab.create",
    ),
    path(
        "/schedule/solar/create/",
        views.SolarScheduleCreateView.as_view(),
        name="schedule.solar.create",
    ),
    path(
        "/schedule/interval/create/",
        views.IntervalScheduleCreateView.as_view(),
        name="schedule.interval.create",
    ),
    path(
        "/schedule/clocked/create/",
        views.ClockedScheduleCreateView.as_view(),
        name="schedule.clocked.create",
    ),
]

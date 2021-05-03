from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("schedule/cron/", views.CrontabView.as_view()),
    path("schedule/interval/", views.IntervalView.as_view()),
    path("schedule/clock/", views.ClockedView.as_view()),
    path("schedule/solar/", views.SolarView.as_view()),
    path("task/create/", views.TaskView.as_view()),
]

from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("schedule/cron/", views.CrontabView.as_view()),
    path("schedule/interval/", views.IntervalView.as_view()),
    path("schedule/clock/", views.ClockedView.as_view()),
    path("schedule/solar/", views.SolarView.as_view()),
    path("task/", views.TaskView.as_view()),
    path("task/<int:task_id>/run/", views.run_task, name="run_task"),
    path("task/<str:task_id>/result/", views.TaskResultView.as_view()),
    path("task/<int:task_id>/delete/", views.TaskDeleteView.as_view()),
]

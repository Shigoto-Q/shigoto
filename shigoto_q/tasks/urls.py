from __future__ import absolute_import

from django.urls import path

from shigoto_q.tasks import views

app_name = "tasks"

urlpatterns = [
    path("schedule/cron/", views.CrontabView.as_view()),
    path("schedule/interval/", views.IntervalView.as_view()),
    path("schedule/clock/", views.ClockedView.as_view()),
    path("schedule/solar/", views.SolarView.as_view()),
    path("task/", views.TaskView.as_view(), name="shigoto.tasks.create-task"),
    path("task/<int:task_id>/run/", views.RunTaskView.as_view()),
    path("task/<str:task_id>/result/", views.TaskResultView.as_view()),
    path("task/<int:task_id>/delete/", views.TaskDeleteView.as_view()),
    path(
        "task/<int:task_id>/update/",
        views.TaskUpdateView.as_view(),
        name="shigoto.tasks.update-task",
    ),
    path("task/types/", views.TaskTypeView.as_view()),
]

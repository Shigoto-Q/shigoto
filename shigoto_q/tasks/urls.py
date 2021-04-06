from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [path("cron/", views.CrontabView.as_view())]

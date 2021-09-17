from django.urls import path
from shigoto.views import AdminConfigView

app_name = "users"

urlpatterns = [path("admin-config/", AdminConfigView.as_view(), name="user-list")]

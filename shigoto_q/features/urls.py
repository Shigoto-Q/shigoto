from django.urls import path

from shigoto_q.features import views

app_name = "features"

urlpatterns = [
    path(
        "features/urls/",
        views.URLListView.as_view(),
        name="features.urls",
    ),
]

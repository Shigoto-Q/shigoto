from django.urls import path
from .api import views

app_name = "users"
urlpatterns = [path("products/", views.ProductView.as_view())]

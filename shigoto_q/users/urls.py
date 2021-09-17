from django.urls import path

from .api import views
from .views import create_checkout, create_customer_sub, my_webhook_view

app_name = "users"

urlpatterns = [
    path("products/", views.ProductView.as_view()),
    path("hooks/", my_webhook_view),
    path("create_customer/", create_customer_sub, name="create_customer_sub"),
    path("create-checkout-session/", create_checkout, name="create_checkout"),
    path("jwt/verify/", views.CustomJwtView.as_view(), name="custom_view_jwt"),
]

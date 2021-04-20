from django.urls import path

from .api import views
from .views import (
    my_webhook_view,
    create_customer_sub,
    create_checkout,
)

app_name = "users"

urlpatterns = [
    path("products/", views.ProductView.as_view()),
    path("hooks/", my_webhook_view),
    path("create_customer/", create_customer_sub, name="create_customer_sub"),
    path("create-checkout-session/", create_checkout, name="create_checkout"),
]

from django.urls import path

from shigoto_q.products import views
from shigoto_q.products import webhooks

app_name = "products"

urlpatterns = [
    path(
        "customer/subscription/create/",
        views.CustomerSubscriptionView.as_view(),
        name="customer.subscription.create",
    ),
    path(
        "customer/subscription/session/create/",
        views.SessionView.as_view(),
        name="customer.subscription.session.create",
    ),
    path(
        "subscription/webhook/",
        webhooks.subscription,
        name="webhook",
    )
]

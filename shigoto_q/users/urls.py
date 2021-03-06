from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from shigoto_q.users.api import views as api_views
from shigoto_q.users.views import UserLogoutView, CreateOTPView

app_name = "users"

urlpatterns = [
    path("user/logout", UserLogoutView.as_view(), name="shigoto_q.users.logout"),
    path(
        "user/<str:user>/",
        api_views.UserView.as_view(),
        name="shigoto_q.users.api.user",
    ),
    path(
        "users/",
        api_views.UserCreateView.as_view(),
        name="shigoto_q.users.api.user.create",
    ),
    path(
        "users/list/",
        api_views.UsersListView.as_view(),
        name="shigoto_q.users.api.users.list",
    ),
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="shigoto_q.users.token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="shigoto_q.users.token_refresh",
    ),
    path(
        "users/subscribe/",
        api_views.SubscriberView.as_view(),
        name="shigoto_q.user.subscribe",
    ),
    path(
        "users/unsubscribe/",
        api_views.UnsubscribeView.as_view(),
        name="shigoto_q.user.unsubscribe",
    ),
    path(
        "user/otp/create/",
        CreateOTPView.as_view(),
        name="shigoto_q.user.otp",
    ),
]

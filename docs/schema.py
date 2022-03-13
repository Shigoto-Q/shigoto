from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Shigoto API",
        default_version="v1",
        description="Shigoto is a cron, scheduled task management cloud based solution.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="aleksov_s@outlook.com"),
        license=openapi.License(name="GNU GENERAL PUBLIC LICENSE"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

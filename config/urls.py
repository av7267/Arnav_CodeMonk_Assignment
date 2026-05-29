from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Django admin panel
    path(
        "admin/",
        admin.site.urls,
    ),

    # Authentication APIs
    path(
        "api/v1/auth/",
        include("apps.users.urls"),
    ),

    # Paragraph processing APIs
    path(
        "api/v1/paragraphs/",
        include("apps.paragraphs.urls"),
    ),

    # OpenAPI schema generation
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    # Swagger documentation UI
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),
]
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings

...

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("appointments/", include("appointments_app.urls")),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("reports/", include("reports_app.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "swagger-download/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path("statistics/", include("statistics_app.urls")),
    path("users/", include("users_app.urls")),
    path("video-call/", include("video_call.urls")),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .generator import BothHttpAndHttpsSchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
        title="File collector",
        default_version="v1",
        description="Minfin",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="info@imv.uz"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    generator_class=BothHttpAndHttpsSchemaGenerator,
    permission_classes=(permissions.AllowAny,),
)

# Conditionally include Swagger/Redoc URLs based on IS_API_PROTECTED setting
# If API is protected, hide all Swagger/Redoc documentation
if getattr(settings, 'IS_API_PROTECTED', False):
    swagger_urlpatterns = []
else:
    swagger_urlpatterns = [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]

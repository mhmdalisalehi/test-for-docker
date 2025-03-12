from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Cryptocurrency API",
        default_version="v1",
        description="Brief descriptions about the api",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="Mohammadroudbari2gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# for testing sentry

def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    # urls of the admin panel
    path("admin/", admin.site.urls),
    # url inclusion of the app
    # path("", include("website.urls")),
    # testing sentry logger
    path("sentry-debug/", trigger_error),
]

# if this is enable instead of seeing the project you will see a page which shows a simple text as you will be launching soon
if settings.COMINGSOON:
    urlpatterns.insert(
        0, re_path(r"^", TemplateView.as_view(template_name="comingsoon.html"))
    )


# serving medias and static files in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# showing debugger toolbar when you are using debug mode
if settings.SHOW_DEBUGGER_TOOLBAR:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]


# showing swagger and restframework api authentications
if settings.SHOW_SWAGGER:
    urlpatterns += [
        path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
        path(
            "swagger/api.json",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]

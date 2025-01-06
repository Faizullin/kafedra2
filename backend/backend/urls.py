from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views import defaults as default_views
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog

admin.site.site_header = "Dj-LMS Admin"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    # path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    # path("", include("apps.core.urls")),
    # path("jet/", include("jet.urls", "jet")),  # Django JET URLS
    # path(
    #     "jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")
    # ),  # Django JET dashboard URLS
    # path("accounts_/", include("apps.accounts.urls")),
    # path("programs/", include("apps.courses.urls")),
    # path("results/", include("apps.results.urls")),
    # path("search/", include("apps.search.urls")),
    # path("quiz/", include("apps.quiz.urls")),
    # path("payments/", include("apps.payments.urls")),
    # path("accounts_/api/", include("apps.accounts.api.urls", namespace="accounts_-api")),
)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]

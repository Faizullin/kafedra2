import django
from django.apps import apps
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views
from django.urls import include, path
from lms.views import handler403, handler404, handler500

# from apps.sitemaps import base_sitemaps TODO: add

admin.autodiscover()

admin.site.site_header = "Dj-LMS Admin"

urlpatterns = [
    # Include admin as convenience. It's unsupported and only included
    # for developers.
    path('admin/', admin.site.urls),

    # i18n URLS need to live outside of i18n_patterns scope of Oscar
    path('i18n/', include(django.conf.urls.i18n)),

    # # include a basic sitemap  TODO: add
    # path('sitemap.xml', views.index,
    #     {'sitemaps': base_sitemaps}),
    # path('sitemap-<slug:section>.xml', views.sitemap,
    #     {'sitemaps': base_sitemaps},
    #     name='django.contrib.sitemaps.views.sitemap')
]

# Prefix Oscar URLs with language codes
urlpatterns += i18n_patterns(
    path('', include(apps.get_app_config('lms').urls[0])),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Server statics and uploaded media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Allow error pages to be tested
    urlpatterns += [
        path('403', handler403, {'exception': Exception()}),
        path('404', handler404, {'exception': Exception()}),
        path('500', handler500),
    ]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()

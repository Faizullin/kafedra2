from django.conf import settings
from django.urls import path
from django.utils.translation import gettext_lazy as _

from apps.pages.views import HomeView
from lms.core.application import LmsConfig


class PagesConfig(LmsConfig):
    label = "pages"
    name = "lms.apps.pages"
    verbose_name = _("Pages")

    namespace = "pages"

    # pylint: disable=attribute-defined-outside-init, reimported, unused-import
    def ready(self):
        self.home_view = HomeView

    def get_urls(self):
        urls = [
            path(settings.LMS_HOMEPAGE_URL, self.home_view.as_view(), name="home"),
        ]

        return self.post_process_urls(urls)

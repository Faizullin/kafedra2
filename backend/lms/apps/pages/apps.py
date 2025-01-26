from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.conf import settings

from lms.core.application import LmsConfig
from lms.core.loading import get_class


class PagesConfig(LmsConfig):
    label = "pages"
    name = "lms.apps.pages"
    verbose_name = _("Pages")

    namespace = "pages"

    # pylint: disable=attribute-defined-outside-init, reimported, unused-import
    def ready(self):
        self.home_view = get_class("pages.views", "HomeView")

    def get_urls(self):
        urls = [
            path(settings.LMS_HOMEPAGE_URL, self.home_view.as_view(), name="home"),
        ]

        return self.post_process_urls(urls)

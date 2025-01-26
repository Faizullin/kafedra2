from django.urls import path
from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig
from lms.core.loading import get_class


class WishlistsConfig(LmsConfig):
    label = "wishlists"
    name = "lms.apps.wishlists"
    verbose_name = _("Wishlists")

    namespace = "wishlists"

    # pylint: disable=attribute-defined-outside-init
    def ready(self):
        self.wishlist_view = get_class("wishlists.views", "WishListView")

    def get_urls(self):
        urls = [
            path("<str:key>/", self.wishlist_view.as_view(), name="detail"),
        ]

        return self.post_process_urls(urls)

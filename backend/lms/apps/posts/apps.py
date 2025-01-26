from django.utils.translation import gettext_lazy as _

from lms.core.application import LmsConfig


class PostsConfig(LmsConfig):
    label = "posts"
    name = "lms.apps.posts"
    verbose_name = _("Posts")

    namespace = "posts"

    # pylint: disable=attribute-defined-outside-init, unused-import
    def ready(self):
        super().ready()

    def get_urls(self):
        urls = super().get_urls()
        return self.post_process_urls(urls)

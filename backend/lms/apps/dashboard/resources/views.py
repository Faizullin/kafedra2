from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic

from lms.core.loading import get_model

Post = get_model("posts", "Post")


class ResourcesPostListView(generic.TemplateView):
    template_name = "lms/dashboard/resources/post_list.html"


class ResourcesPostDeleteView(generic.DeleteView):
    """
    Dashboard view to delete a product. Has special logic for deleting the
    last child product.
    Supports the permission-based dashboard.
    """

    template_name = "lms/dashboard/resources/post_delete.html"
    model = Post
    context_object_name = "post"

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        msg = _("Deleted post '%s'") % self.object.title
        messages.success(self.request, msg)
        return reverse("dashboard:resources-post-list")

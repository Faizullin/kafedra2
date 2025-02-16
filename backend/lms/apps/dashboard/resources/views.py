from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic import DetailView
from rest_framework.reverse import reverse_lazy

from lms.apps.dashboard.resources.url_reverses import url_reverses_dict
from lms.core.loading import get_model, get_classes
from lms.crud_base.tables import Table, Column, ActionsColumn, DefaultEditAction
from lms.crud_base.views import BaseCreateView, BaseUpdateView, get_default_add_success_message, \
    get_default_update_success_message, BaseListView

Post = get_model("posts", "Post")
PostForm, = get_classes(
    "dashboard.resources.forms", ["PostForm", ]
)


class ResourcesPostListView(BaseListView):
    model = Post
    page_list_url = reverse_lazy("dashboard:resources-post-list")

    class PostTable(Table):
        id = Column(field_name="id", header="#", orderable=True)
        title = Column(field_name="title")
        question_type = Column(field_name="question_type")
        category = Column(field_name="category.title", header=_("Category"), orderable=False, searchable=False)
        author = Column(field_name="author.username", header=_("Author"), orderable=False, searchable=False)
        actions = ActionsColumn(
            actions=[
                DefaultEditAction(
                    redirect_url_name=url_reverses_dict["resources-post-update"],
                ),
            ],
        )

        class Meta:
            model = Post
            source_url = reverse_lazy('dashboard:resources-post-list-api')
            fields = ['id', 'title', 'category', 'author', 'actions']

    table = PostTable()

    def get_urls(self):
        return {
            'add': reverse('dashboard:resources-post-create'),
        }


class ResourcesPostCreateView(BaseCreateView):
    model = Post
    form_class = PostForm
    page_list_url = reverse_lazy("dashboard:resources-post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_type = "posts"
        return super().form_valid(form)

    def get_success_message(self, obj):
        return get_default_add_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("dashboard:resources-post-update", pk=self.object.pk)

    def get_urls(self):
        return {}


class ResourcesPostUpdateView(BaseUpdateView):
    model = Post
    form_class = PostForm
    page_list_url = reverse_lazy("dashboard:resources-post-list")

    def get_success_message(self, obj):
        return get_default_update_success_message(obj.title, obj.id)

    def get_success_url(self):
        return resolve_url("dashboard:resources-post-update", pk=self.object.pk)

    def get_urls(self):
        return {}


class ResourcesPostEditContentView(DetailView):
    template_name = "lms/dashboard/resources/post_edit_content.html"
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        js_src_list = [
            "https://cdn.jsdelivr.net/npm/@editorjs/editorjs@latest",
        ]
        PLUGINS = (
            '@editorjs/paragraph',
            '@editorjs/image',
            '@editorjs/header',
            '@editorjs/list',
            '@editorjs/checklist',
            '@editorjs/quote',
            '@editorjs/raw',
            '@editorjs/code',
            '@editorjs/inline-code',
            '@editorjs/embed',
            '@editorjs/delimiter',
            '@editorjs/warning',
            '@editorjs/link',
            '@editorjs/marker',
            '@editorjs/table',
        )
        for i in PLUGINS:
            js_src_list.append("https://cdn.jsdelivr.net/npm/{}@latest".format(i))

        instance = context["object"]
        title = "{} {} [{}]".format(_("Edit"), _("Post"), str(instance.pk))
        ct_type = ContentType.objects.get_for_model(instance)
        context.update({
            'title': title,
            'page_header_title': title,
            'card_header_title': "{} [{}]".format(instance.title, instance.pk),
            'breadcrumbs': [
                {"label": _("Dashboard"), "url": resolve_url("dashboard:index")},
                {"label": _("Posts"), "url": resolve_url("dashboard:resources-post-list")},
                {"label": title, "url": resolve_url("dashboard:resources-post-update", pk=instance.pk)},
                {"label": _("Edit Content"), "current": True},
            ],
            "editor": {
                "media": {
                    "js": js_src_list,
                    "css": (),
                },
                "content_type": ct_type.model,
                "object_id": instance.pk,
                "to_model_field_name": "content",
                "value": instance.content,
            },
            "instance": instance,
            "attachments": {
                "content_type": ct_type.model,
                "object_id": instance.pk,
            },
        })
        return context


class ResourcesPostDeleteView(generic.DeleteView):
    template_name = "lms/dashboard/resources/post_delete.html"
    model = Post

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        msg = _("Deleted post '%s'") % self.object.title
        messages.success(self.request, msg)
        return reverse("dashboard:resources-post-list")

from crispy_forms.layout import Layout, Submit, Row, Column, Button
from django.shortcuts import resolve_url
from django.utils.translation import gettext_lazy as _

from lms.core.loading import get_model
from lms.crud_base.fields import ThumbnailAttachmentField
from lms.crud_base.forms import BaseForm

Post = get_model("posts", "Post")


class PostForm(BaseForm):
    thumbnail = ThumbnailAttachmentField(help_text=_("Asynchronous save."), required=False)

    class Meta:
        model = Post
        fields = (
            "title",
            "publication_status",
            "category",
            "thumbnail",
        )

    def get_crisply_layout(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        content_editor_link_btn = Button(
            "edit-content-redirect-btn",
            _("Edit Content"),
            css_class="btn-secondary",
            onClick="window.location.href='{}'".format(
                resolve_url("dashboard:resources-post-edit-content", pk=instance.pk)) if instance else "",
            disabled=not bool(instance),
        )
        return Layout(
            Row(
                Column('title', css_class='col-md-6 mb-3'),
                Column('publication_status', css_class='col-md-6 mb-3'),
                Column('category', css_class='col-md-6 mb-3'),
                Column('thumbnail', css_class='col-md-6 mb-3'),
                Column(
                    Submit('submit', _('Save'), css_class='btn-primary'),
                    content_editor_link_btn,
                    css_class='col-md-6 mb-3'
                ),
            ),
        )

    def init_add_page_disabled(self, *args, **kwargs):
        if not kwargs['instance']:
            self.fields["thumbnail"].disabled = True

from django import forms

from apps.posts.models import Post


# news and events
class NewsAndEventsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "publication_status",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["content"].widget.attrs.update({"class": "form-control"})
        self.fields["publication_status"].widget.attrs.update({"class": "form-control"})
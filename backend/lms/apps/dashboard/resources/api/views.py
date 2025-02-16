from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from rest_framework import generics

from apps.dashboard.quiz.api.views import BaseListApiView
from lms.apps.dashboard.editor.api.views import BaseContentEditorActionAPIView
from lms.core.loading import get_model
from .serializers import PostSerializer, TagSerializer

Post = get_model("posts", "Post")
Tag = get_model("posts", "Tag")


##########################################################
# Posts
# ########################################################
class ResourcesPostListAPIView(BaseListApiView):
    serializer_class = PostSerializer
    search_fields = ['title', 'content']

    class PostFilter(FilterSet):
        title = CharFilter(lookup_expr='icontains')

        class Meta:
            model = Post
            fields = ['id', 'title', 'publication_status', 'category', 'author']

    filterset_class = PostFilter

    def get_queryset(self):
        queryset = Post.objects.all().prefetch_related('author', 'category', 'thumbnail')
        return queryset


class ResourcesPostEditContentActionAPIView(BaseContentEditorActionAPIView):
    pass


class TagListAPIView(BaseListApiView):
    serializer_class = TagSerializer
    search_fields = ['title']

    def get_queryset(self):
        queryset = Tag.objects.all()
        return queryset

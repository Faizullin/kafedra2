from django_filters import CharFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from lms.core.loading import get_model
from .filters import CustomPagination
from .serializers import PostSerializer

Post = get_model("posts", "Post")


class BaseListApiView(generics.ListAPIView):
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['id', 'created_at', 'updated_at']
    filterset_class = None


class BaseDestroyApiView(generics.DestroyAPIView):
    lookup_field = "id"


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

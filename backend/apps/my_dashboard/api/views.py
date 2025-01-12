from django_filters.rest_framework import DjangoFilterBackend, CharFilter, FilterSet
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.posts.models import Post
from .filters import CustomPagination
from .serializers import PostSerializer


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
class PostListAPIView(BaseListApiView):
    serializer_class = PostSerializer
    search_fields = ['title', 'content']

    class PostFilter(FilterSet):
        title = CharFilter(lookup_expr='icontains')

        class Meta:
            model = Post
            fields = ['id', 'title', 'publication_status', 'category']

    filterset_class = PostFilter
    queryset = Post.objects.all()


class PostDestroyView(BaseDestroyApiView):
    queryset = Post.objects.all()
    model = Post


##########################################################
# Courses
# ########################################################
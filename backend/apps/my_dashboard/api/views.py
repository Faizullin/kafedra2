from django_filters.rest_framework import DjangoFilterBackend, CharFilter, FilterSet
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.posts.models import Post
from apps.quiz.models import Quiz, QuestionGroup
from .filters import CustomPagination
from .serializers import PostSerializer, CourseSerializer, QuizSerializer
from ...courses.models import Course


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
class CourseListAPIView(BaseListApiView):
    serializer_class = CourseSerializer
    search_fields = ['title', 'content']

    class CourseFilter(FilterSet):
        title = CharFilter(lookup_expr='icontains')

        class Meta:
            model = Course
            fields = ['id', 'title', 'publication_status', 'category']

    filterset_class = CourseFilter
    queryset = Course.objects.all()


##########################################################
# Quizzes
# ########################################################
class QuizListAPIView(BaseListApiView):
    serializer_class = QuizSerializer
    search_fields = ['title', ]

    class QuizFilter(FilterSet):
        title = CharFilter(lookup_expr='icontains')

        class Meta:
            model = Quiz
            fields = ['id', 'title', 'publication_status', ]

    filterset_class = QuizFilter
    queryset = Quiz.objects.all()


class QuizDestroyView(BaseDestroyApiView):
    queryset = Quiz.objects.all()
    model = Quiz


##########################################################
# QuestionGroups
# ########################################################
class QuizQuestionGroupCreateAPIView(generics.CreateAPIView):
    queryset = QuestionGroup.objects.all()


class QuizQuestionGroupUpdateAPIView(generics.UpdateAPIView):
    queryset = QuestionGroup.objects.all()
